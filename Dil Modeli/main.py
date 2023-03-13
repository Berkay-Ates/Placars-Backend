from joblib import load

#pip install scikit-learn 1.2.2
#pip install joblib 1.2.0
#pip install scipy 1.10.1 Kütüphanelerini Yükle.  print(scipy.__version__) ile kontrol et.
#Python 3.8.0 64 Bit test edildi.

def control(input_data):
    input_data = [input_data]
    model = load('model.joblib')
    predictions = model.predict(input_data)
    probabilities = model.predict_proba(input_data)[:, 1]
    return predictions, probabilities


def main():
    test = "PLACARS uygulaması Her Yerde."
    result = control(test) #String değer gönderilir
    print(result) #1. Değer FALSE = uygun , TRUE = uygun değil | 2. Değer uygun olmama olasılığı


    """ # kontrol icin import joblib, scipy, sklearn, sys
    print(scipy.__version__)
    print(sklearn.__version__)
    print(joblib.__version__)
    print(sys.version)
    """

if __name__ == '__main__':
    main()