from nsfw_detector import predict


# Baska bir dosyadan bunu importladiktan sonra NSFWDetector().get_biggest_value(imgpath) yazarsan gorselin tipini returnler.
# Calismiyorsa ya model pathte ya da imgpathde sıkıntı olabilir.
class NSFWDetector:
    def __init__(self, model_path=None):
        if model_path is None:
            model_path = "./nsfw_mobilenet2.224x224.h5"
        self.model = predict.load_model(model_path)
        self.imgpath = None
        self.result = None

    def predict(self, imgpath):
        self.imgpath = imgpath
        self.result = predict.classify(self.model, imgpath)
        return self.result

    def get_biggest_value(self, imgpath):
        self.imgpath = imgpath
        self.result = predict.classify(self.model, imgpath)
        return max(
            self.result[self.imgpath], key=lambda key: self.result[self.imgpath][key]
        )
