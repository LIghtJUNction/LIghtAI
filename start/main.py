def main():
    train_dataset = load_and_preprocess_data('imdb', split='train[:10%]')
    eval_dataset = load_and_preprocess_data('imdb', split='test[:10%]')

    model = load_model().to('cuda')

    train(model, train_dataset, epochs=3, batch_size=8)
    evaluate(model, eval_dataset, batch_size=8)

if __name__ == "__main__":
    main()
