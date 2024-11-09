import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import os
from torch.utils.data import DataLoader
import tqdm
import logging

from lxfx.data import TimeSeriesDatasetManager
from lxfx.utils import createLogger
from lxfx.metrics import RMSELoss

class ModelTrainer():
    def __init__(self, 
                model = None,
                dataset_manager:TimeSeriesDatasetManager = None,
                train_dataloader:DataLoader = None,
                loss_fn = None,
                optmizer = None,
                epochs = 3,
                validation_dataloader:DataLoader = None,
                test_dataloader = None,
                accuracy_fn = None,
                device = None, 
                lr= 0.001,
                project_path = None, 
                is_logging = True,
                resume = False,
                targets_transformed = False):
        """Class to handle training of the model on a train data from the data_dataloader and validation data from
        the validation_dataloader.
        Parameters:
            model: model to undergo training
            dataset_manager: The datasetManager used to generate the dataloaders
            train_dataloader: The dataloader that is supposed to load the training feature and labels
            loss_fn: Loss function to be used. e.g loss_fn = MSELoss(), fit(loss_fn = loss_fn), This can also be a function
            optmizer: The optmizimzer to be used to edit  the model parameters
            epochs: Number of times to train the model on the data (num of different times the model has to see the data)
            validation_dataloader: Dataloader that is to load the validation data.
            test_dataloader: Dataloader thtat is to load the test data for prediction.
            accuracy_fn: The accuracy function or class to be used.
            device: Connects to a gpu if available by default you can override this behaviour.
            lr: The learning rate to be used by the optimizer. Defaults to 0.001
            project_path: This is the path to the directory where the best model is to be saved, results and so on as the model is training
            is_logging: whether to log training and other kinds of information into a file in the project dir path
            resume: Whether to resume training from the last saved model.
            targets_transformed: Wether or not the targets were transformed
        Examples:
            >>> train_dataloader = DataLoader(train_dataset, shuffle = False, batch_size = 32)
            >>> validation_dataloader = DataLoader(val_dataset, shuffle = False, batch_size = 32)
            >>> test_dataloader = DataLoader(test_dataset, shuffle = False, batch_size= len(test_dataset))
            >>> loss_fn = "mse" or MSELoss()
            >>> optimizer = "adam" or Adam(model.paramters(), lr = 0.001)
            >>> device = torch.device("gpu") if torch.cuda.is_available() else torch.device("cpu")
        """
        self.console_logger = createLogger(logging.INFO, is_consoleLogger=True)

        self.model = model
        self.loaded_model = None
        self.targets_transformed= targets_transformed
        self.dataset_manager = dataset_manager 

        if self.dataset_manager:
            self.train_dataloader, self.validation_dataloader, self.test_dataloader = self.dataset_manager.dataloaders()
            self.targets_transformed = self.dataset_manager.transform_targets
        else:
            self.train_dataloader = train_dataloader
            self.validation_dataloader = validation_dataloader
            self.test_dataloader = test_dataloader

        self.loss_fn = loss_fn
        self.getloss_fn()

        self.optmizer = optmizer
        self.optim_lr = lr
        self.getOptimizer()

        self.acc_fn = accuracy_fn
        self.epochs = epochs

        self.device = torch.device("gpu") if torch.cuda.is_available() else torch.device("cpu")
        self.model.to(self.device)
        self.stat_logs = {}
        self.resume = resume

        self.min_loss_ = float('inf')
        self.project_path = project_path
        if self.project_path:
            self.project_path = self.getLoggingDir()
        self.is_logging = is_logging
        if not self.project_path:
            self.is_logging = False
        self.bestModelPath = os.path.join(self.project_path, "best.pth") if self.project_path else None
        self.lastModelPath = os.path.join(self.project_path, "last.pth") if self.project_path else None
        
        if not self.resume:
            if self.bestModelPath:
                if os.path.exists(self.bestModelPath):
                    os.remove(self.bestModelPath)
                if os.path.exists(self.lastModelPath):
                    os.remove(self.lastModelPath)
        self.training_logs = {
            "stat_logs":{},
            "min_loss_":self.min_loss_,
            "optmizer":None,
            "loss_fn":None
        }
        self.early_stopping_counte = 0
        self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(self.optmizer, "min", patience=2, verbose=True)# change the learning rage based on the validation loss i.e if the val loss does not improve for 2 epochs then reduce the learning rate by half

        if self.project_path:
            self.trainLogger_filepath= os.path.join(self.project_path, "training_logs.txt")
            self.training_file_logger = createLogger(log_level=logging.INFO,
                                                    name="trainingLogger",
                                                    filename= self.trainLogger_filepath)


    def getLoggingDir(self):
        # Get the directory where to log all the obtained information including models, weights, results, images and so on 
        if self.project_path:
            available_dirs = os.listdir(self.project_path)
            if len(available_dirs) != 0:
                paths = list(map(lambda x : os.path.join(self.project_path, x), available_dirs))
                train_dir_count = 0
                for path in paths:
                    if os.path.isdir(path):
                        if "train" in path:
                            count = int(path.split("_")[-1])
                            if count > train_dir_count:
                                train_dir_count = count
                train_dir_name = "/Train_"+str(train_dir_count+1)
            else:
                train_dir_name  = "/Train_1"
            logging_dir =  os.path.join(self.project_path, train_dir_name)
            try:
                os.mkdir(logging_dir)
                return logging_dir
            except PermissionError as e:
                self.console_logger.warning(f"The program does not have enough permissios to create a directory in path {self.project_path}. Consider changing permissions.")
                return self.project_path 

    def getloss_fn(self):
        if self.loss_fn == "mse":
            self.loss_fn = nn.MSELoss()
        elif self.loss_fn == "rmse":
            self.loss_fn = RMSELoss()

    def getOptimizer(self):
        if self.optmizer == "adam":
            self.optmizer = optim.Adam(params = self.model.parameters(), lr=self.optim_lr)

    def resume(self, ):
        """
        Resumes the training of the model from the last saved model.
        """
        pass 

    def computeLoss(self, features, labels, train = False):
        features, labels = features.to(self.device), labels.to(self.device)
        preds = self.model(features)

        # transform the preds if the targets weren't transformed
        if not self.targets_transformed:
            preds = self.dataset_manager.inverse_targets(preds, is_training = True)

        loss = self.loss_fn(preds, labels)
        if train:
            loss.backward()
            nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0) # gradient clipping
        if isinstance(loss, torch.Tensor):
            loss = loss.item()
        if self.acc_fn:
            acc = self.acc_fn(preds.cpu(), labels.cpu())
            if isinstance(acc, torch.Tensor):
                acc = acc.item()
            return loss, acc
        return loss, None

    def evaluateModel(self, testDataLoader:DataLoader):
        """
        Evaluates the model on the test data.

        Parameters:
            testDataLoader (DataLoader): The dataloader that is supposed to load the test data.

        Returns:
            avg_loss (float): The average loss of the model on the test data.
            avg_acc (float): The average accuracy of the model on the test data.
        """
        self.model.eval()
        with torch.inference_mode():
            total_loss = 0
            total_acc = 0
            for idx, (features, labels) in enumerate(testDataLoader):
                loss, acc = self.computeLoss(features, labels)
                total_loss += loss
                if self.acc_fn:
                    total_acc += acc
            avg_loss = total_loss / len(testDataLoader)
            if self.acc_fn:
                avg_acc = total_acc / len(testDataLoader)
                print(f"Test Loss: {avg_loss:.5f}, Test Acc: {avg_acc:.5f}")
            else:
                print(f"Test Loss: {avg_loss:.5f}")
        return avg_loss, avg_acc

    def validateModel(self):
        self.model.eval()
        with torch.inference_mode():
            total_loss = 0
            total_acc = 0
            for idx, (features, labels) in enumerate(self.validation_dataloader):
                loss, acc = self.computeLoss(features, labels)
                total_loss += loss
                if self.acc_fn:
                    total_acc += acc
            avg_loss = total_loss / len(self.validation_dataloader)
            avg_acc = total_acc / len(self.validation_dataloader) if self.acc_fn else None
        return avg_loss, avg_acc

    def trainModel(self, epochs = None, verbose_level = "min"):
        """
        Trains the model on the train data.

        Parameters:
            epochs (int): The number of epochs to train the model.
            verbose (bool): Whether to show alot of training steps per epoch
            verbose_level( one if min, mid, max): how much of logging inf to show on the screen
        Returns:
            train_loss_history (list): The history of the training loss.
            train_acc_history (list): The history of the training accuracy.
            val_loss_history (list): The history of the validation loss.
            val_acc_history (list): The history of the validation accuracy.
        """
        train_loss_history = []
        train_acc_history = []
        val_loss_history = []
        val_acc_history = []
        if verbose_level == "max":
            display_steps = len(self.train_dataloader)//10 
        elif verbose_level == "mid":
            display_steps = len(self.train_dataloader)//0
        else: # min falls under here
            display_steps = None
        self.epochs= epochs
        for epoch in tqdm.tqdm(range(0, self.epochs)):
            print(f"Epoch: {epoch}")
            self.model.train()
            epoch_total_loss = 0
            epoch_total_acc = 0
            for idx, (features, labels) in enumerate(self.train_dataloader):
                self.optmizer.zero_grad()
                train_loss, train_acc = self.computeLoss(features, labels, train = True)
                epoch_total_loss += train_loss
                if self.acc_fn:
                    epoch_total_acc += train_acc
                self.optmizer.step()

                if self.acc_fn:
                    step_log_info = f"\tStep: {idx}/{len(self.train_dataloader)} Train Loss: {train_loss:.5f}, Train Acc: {train_acc:.5f}"
                    if display_steps:
                        if idx % display_steps == 0:
                            print(step_log_info)
                else:
                    step_log_info = f"\tStep: {idx}/{len(self.train_dataloader)} Train Loss: {train_loss:.5f}"
                    if display_steps:
                        if idx % display_steps == 0:
                                print(step_log_info)

                if self.project_path and self.is_logging:
                    self.training_file_logger.info(step_log_info)

            val_loss, val_acc = self.validateModel()

            train_loss = epoch_total_loss / len(self.train_dataloader)
            train_acc = epoch_total_acc / len(self.train_dataloader) if self.acc_fn else None

            train_loss_history.append(train_loss)
            val_loss_history.append(val_loss)

            self.scheduler.step(val_loss) # learning rate scheduling

            if self.acc_fn:
                train_acc_history.append(train_acc)
                val_acc_history.append(val_acc)
                epoch_log_info = f"Epoch: {epoch+1}, Train Loss: {train_loss:.5f}, Train Acc: {train_acc:5f}, Val Loss: {val_loss:.5f}, Val Acc: {val_acc:.5f}"
                print(epoch_log_info)
            else:
                epoch_log_info = f"Epoch: {epoch+1}, Train Loss: {train_loss:.5f}, Val Loss: {val_loss:.5f}"
                print(epoch_log_info)

            if self.project_path and self.is_logging:
                self.training_file_logger.info(epoch_log_info)  

            if val_loss < self.min_loss_:
                print(f"Model val_loss improved from {self.min_loss_} to {val_loss}")
                self.min_loss_ = val_loss
                if self.project_path:
                    torch.save(self.model, self.bestModelPath)
                    print(f"Model Saved to file: {self.bestModelPath}")
            else:
                print(f"Model val_loss did not improve from {self.min_loss_}")
        self.stat_logs["train_loss_history"] = train_loss_history
        self.stat_logs["train_acc_history"] = train_acc_history 
        self.stat_logs["val_loss_history"] = val_loss_history 
        self.stat_logs["val_acc_history"] = val_acc_history
        return train_loss_history, train_acc_history, val_loss_history, val_acc_history

    def visualizeResults(self, dirpath = None, show= True, format = None, figsize = (15, 20)):
        """ 
        visualize the results from the training and or save them
        Parameters:
            dirpath: The directory to which to save the image files
            show: Whether or not to show the images.
            format: file format to which to save the files. Default is png
            figsize: The figure size to use when plotting eg figsize = (15, 20) #<== default
        """
        fig1 = plt.figure(figsize = figsize)

        # loss vs epochs 
        if self.stat_logs:
            axs1 =fig1.add_subplot(1,1,1)
            axs1.plot(range(self.epochs), self.stat_logs["train_loss_history"], label = "train_loss")
            if len(self.stat_logs["val_loss_history"]) != 0:
                axs1.plot(range(self.epochs), self.stat_logs["val_loss_history"], label = "val_loss")
            fig1.legend()
            if dirpath:
                fname = os.path.join(dirpath, "train_and_val_losses_vs_epochs.png")
                fig1.savefig(fname = fname)
            elif self.project_path:
                fname = os.path.join(self.project_path, "train_and_val_losses_vs_epochs.png")
                fig1.savefig(fname = fname)

            # accuracies vs epochs 
            if self.acc_fn:
                fig2 = plt.figure(figsize = figsize)
                axs2 = fig2.add_subplot(1,1,1)
                axs2.plot(range(self.epochs), self.stat_logs["train_acc_history"], label="train_accuracy")
                if len(self.stat_logs["val_loss_history"]) != 0:
                    axs2.plot(range(self.epochs), self.stat_logs["val_acc_history"], label= "val_accuracy")
                fig2.legend()
            if dirpath:
                fname = os.path.join(dirpath, "train_and_val_accuracies_vs_epochs.png")
                fig1.savefig(fname = fname)
            elif self.project_path:
                fname = os.path.join(self.project_path, "train_and_val_accuracies_vs_epochs.png")
                fig1.savefig(fname = fname)

    def predict(self, saved = True):
        """Make prediction from the test data."""
        if saved:
            if self.project_path:
                print(f"Loading model from path: {self.bestModelPath}")
                self.loaded_model = torch.load(self.bestModelPath)
            else:
                print("Project directory not specified")
        else:
            self.loaded_model = self.model

        if len(self.test_dataloader) != 0:
            self.loaded_model.eval()
            outputs = []
            with torch.inference_mode():
                for idx, (slice_, __) in enumerate(self.test_dataloader):
                    output = self.loaded_model(slice_)
                    outputs.append([output.cpu().item()])
            return torch.tensor(outputs)
        return None
