import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import precision_score,recall_score
def classify(path):
	X=[]
	y=[]
	with open(path, 'r') as file:
		for line in file.readlines():
			entry = json.loads(line)
			X.append(entry[0])
			y.append(entry[1])
	print(sum(y))
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
	count_vect = CountVectorizer()
	X_train_counts = count_vect.fit_transform(X_train)
	X_test_counts = count_vect.transform(X_test)
	tfidf_transformer = TfidfTransformer()
	X_train_tfidf=tfidf_transformer.fit_transform(X_train_counts)
	X_test_tfidf=tfidf_transformer.transform(X_test_counts)
	# Naive Bayes
	print( "Naive Bayes")
	clf1 = MultinomialNB().fit(X_train_tfidf, y_train)
	y_pred1 = clf1.predict(X_test_tfidf)
	print("Accuracy: ",accuracy_score(y_test, y_pred1))
	print("Precision: ",precision_score(y_test, y_pred1, average='macro') )
	print("Recall: ",recall_score(y_test, y_pred1, average='macro') )
	# Linear SVM
	print( "SVM")
	clf2 = LinearSVC().fit(X_train_tfidf, y_train)
	y_pred2 = clf2.predict(X_test_tfidf)
	print("Accuracy",accuracy_score(y_test, y_pred2))
	print("Precision: ",precision_score(y_test, y_pred2, average='macro') )
	print("Recall: ",recall_score(y_test, y_pred2, average='macro') )
	plt.title('Sentiment Summary')
	plt.xlabel('Sentiment')
	plt.ylabel('Number of tweets')
	plt.bar(y_test,range(len(y_test)),width=0.5)
	plt.show()
	false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_pred1)
	roc_auc = auc(false_positive_rate, true_positive_rate)
	plt.title('Receiver Operating Characteristic - Naive Bayes')
	plt.plot(false_positive_rate, true_positive_rate, 'b',
	label='AUC = %0.2f'% roc_auc)
	plt.legend(loc='lower right')
	plt.plot([0,1],[0,1],'r--')
	plt.xlim([-0.1,1.2])
	plt.ylim([-0.1,1.2])
	plt.ylabel('True Positive Rate')
	plt.xlabel('False Positive Rate')
	plt.show()

	false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_pred2)
	roc_auc = auc(false_positive_rate, true_positive_rate)
	plt.title('Receiver Operating Characteristic - Linear SVM')
	plt.plot(false_positive_rate, true_positive_rate, 'b',
	label='AUC = %0.2f'% roc_auc)
	plt.legend(loc='lower right')
	plt.plot([0,1],[0,1],'r--')
	plt.xlim([-0.1,1.2])
	plt.ylim([-0.1,1.2])
	plt.ylabel('True Positive Rate')
	plt.xlabel('False Positive Rate')
	plt.show()
	


classify("/home/dhanya/Web Mining/DA/tweet_corpus.json")
