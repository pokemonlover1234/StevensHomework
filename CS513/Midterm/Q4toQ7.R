#Aidan Fischer
#11/7/2023
#CS513 Midterm - Questions 4-7
#I pledge my honor that I have abided by the Stevens Honor

# Define metric printing function

printMetrics <- function(conf_mat, purpose) {
  TP=conf_mat[2,2]
  TN=conf_mat[1,1]
  FP=conf_mat[1,2]
  FN=conf_mat[2,1]
  accuracy = (TP+TN)/(TP+TN+FP+FN);   print(paste("Accuracy of",purpose,":", accuracy))
  recall<-TP/(TP+FN);   print(paste("Recall of",purpose,":", recall))
  precision<- TP/(TP+FP)
  f1<- 2*(precision*recall)/(precision+recall); print(paste("F1 of",purpose,":", f1))
}

rm(list=ls())
library(caTools)
library(class)
library(e1071)
library(caret)
data = read.csv("BP.csv")
data = data[complete.cases(data), ]
#Convert categories to the factor data type
#Maintain typo in given file for consistency
#Convert Smoker column to ordinals by using the labels and ordered parameters of the factor ctor
data$Somker <- factor(data$Somker,levels=c("1- Non-smoker","2- Light","3- Moderate","4- Heavy","5- Very Heavy"),labels=1:5,ordered=TRUE)
data$BP_Status <- factor(data$BP_Status, levels=c("Normal","High"),ordered=FALSE)

#Split the dataset. Use set seed for consistency
set.seed(255)
split = sample.split(data$BP_Status, SplitRatio=0.7)
train = subset(data, split == TRUE)
test = subset(data, split == FALSE)

#Display the first few rows of the training set
head(train)

#Display box and pair plots for Age, Weight, Height
boxplot.default(data$Age)
boxplot.default(data$Weight)
boxplot.default(data$Height)

pairs(data[c("Age","Weight","Height")])

#CART classification
library(rpart)
library(rpart.plot)
library(rattle)
library(RColorBrewer)

#Train a CART on the data, display the CART, then classify the test and train datasets on the classifier and print conf matrices and report metrics.
CART_class<-rpart(BP_Status~.,data=train,method="class",control=rpart.control(minsplit=0,cp=0.007,xval=1000))
rpart.plot(CART_class)
CART_test<-predict(CART_class,test, type="class")
CART_test_conf_mat<-as.matrix(table(Actual=test[,"BP_Status"],CART=CART_test))
CART_train<-predict(CART_class,train, type="class")
CART_train_conf_mat<-as.matrix(table(Actual=train[,"BP_Status"],CART=CART_train))

print(CART_test_conf_mat)
printMetrics(CART_test_conf_mat, "CART test")
print(CART_train_conf_mat)
printMetrics(CART_train_conf_mat, "CART train")

#Naive Bayes
NB_class<-naiveBayes(BP_Status~.,data=train)
print(NB_class)
NB_test<-predict(NB_class,test)
NB_test_conf_mat<-as.matrix(table(Actual=test[,"BP_Status"],NB=NB_test))
NB_train<-predict(NB_class,train)
NB_train_conf_mat<-as.matrix(table(Actual=train[,"BP_Status"],NB=NB_train))

print(NB_test_conf_mat)
printMetrics(NB_test_conf_mat, "Naive Bayes test")
print(NB_train_conf_mat)
printMetrics(NB_train_conf_mat, "Naive Bayes train")

#KNN
KNN_class<-train(BP_Status~.,data=train,method="knn",preProcess=c("center","scale"),tuneLength=10)
print(KNN_class)
KNN_test<-predict(KNN_class,test)
KNN_test_conf_mat<-as.matrix(table(Actual=test[,"BP_Status"],KNN=KNN_test))
KNN_train<-predict(KNN_class,train)
KNN_train_conf_mat<-as.matrix(table(Actual=train[,"BP_Status"],KNN=KNN_train))

print(KNN_test_conf_mat)
printMetrics(NB_test_conf_mat, "KNN test")
print(KNN_train_conf_mat)
printMetrics(KNN_train_conf_mat, "KNN train")

