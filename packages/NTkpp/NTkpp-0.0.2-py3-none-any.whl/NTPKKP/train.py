def train(network, x_train, y_train, loss_func, epochs, optimizer=None):
    for epoch in range(epochs):
        network.backward(x_train, y_train, loss_func)
        for layer in network.layers:
            if hasattr(layer, 'update_weights'):
                layer.update_weights(network.learning_rate, optimizer=optimizer)
        loss_value = loss_func(y_train, network.forward(x_train))
        print(f"Эпоха {epoch + 1}/{epochs}, Потеря: {loss_value:.4f}")
