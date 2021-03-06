class Uno(object):
    
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido

    def mostrar(self):
        print(self.nombre, self.apellido)


class Dos(Uno):

    def __init__(self, nombre, apellido, direccion):
        super().__init__(nombre, apellido)
        self.direccion = direccion

    def mostrar(self):
        print(self.nombre, self.apellido, self.direccion)

    def enviar_correo(self, mail):
        print('enviar mail a', mail)


class Tres(Uno):
    
    def __init__(self, nombre, apellido, mail):
        super().__init__(nombre, apellido)
        self.mail = mail
        self.otro = 123

    def mostrar(self):
        print(self.nombre)
        print(self.apellido)

    def caminiar(self, mail):
        print('enviar mail a', mail)



p = Uno('hola', 'chau')


r = Dos('111', '222', '3333')
r2 = Tres('aaaa', 'bbb', 'ccc')



print(r2.__dict__)

