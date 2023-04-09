from code2vec import code2vec as c2v


def test():
    code2vec_model = "/code2vec/models/java14_model/saved_model_iter8.release"
    c2v("load"=code2vec_model, "--predict")


if __name__ == "__main__":
    test()