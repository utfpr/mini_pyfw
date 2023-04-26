import model


class Informacoes:

    nome = model.Frase(50, 'nome completo')
    bio = model.Texto('biografia')
    ultima_atualizacao = model.Data()


# class Temp:
#     pass


# class Bar:
#     pass