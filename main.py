"""
Посредник (Mediator) - паттерн поведения объектов.

Определяет объект, инкапсулирующий способ взаимодействия множества объектов.
Посредник обеспечивает слабую связанность системы, избавляя объекты от необъодимости явно ссылаться друг на друга
и позволяя тем самым независимо изменять взаимодействия между ними.
"""
class WindowBase(object):
    def show(self):
        raise NotImplementedError()

    def hide(self):
        raise NotImplementedError()


class MainWindow(WindowBase):
    def show(self):
        print('Show MainWindow')

    def hide(self):
        print('Hide MainWindow')


class SettingWindow(WindowBase):
    def show(self):
        print('Show SettingWindow')

    def hide(self):
        print('Hide SettingWindow')


class HelpWindow(WindowBase):
    def show(self):
        print('Show HelpWindow')

    def hide(self):
        print('Hide HelpWindow')


class WindowMediator(object):
    def __init__(self):
        # Инициализация со значением None для каждого окна
        self.windows = {
            'main': None,
            'setting': None,
            'help': None
        }

    def show(self, win):
        # Скрыть все окна, кроме того, которое показываем
        for window in self.windows.values():
            if window is not None and window is not win:
                window.hide()
        win.show()

    def set_main(self, win):
        self.windows['main'] = win

    def set_setting(self, win):
        self.windows['setting'] = win

    def set_help(self, win):
        self.windows['help'] = win


main_win = MainWindow()
setting_win = SettingWindow()
help_win = HelpWindow()

med = WindowMediator()
med.set_main(main_win)
med.set_setting(setting_win)
med.set_help(help_win)

main_win.show()  # Покажем главное окно

med.show(setting_win)
# Скрыть главное окно
# Показать окно настроек

med.show(help_win)
# Скрыть главное окно
# Скрыть окно настроек
# Показать окно помощи

"""
Хранитель (Memento) - паттерн поведения объектов.

Не нарушая инкапсуляции, фиксирует и выносит за пределы объекта его внутреннее состояние так,
чтобы позднее можно было восстановить в нем объект.
"""


class Memento(object):
    """Хранитель"""
    def __init__(self, state):
        self._state = state

    def get_state(self):
        return self._state


class Caretaker(object):
    """Опекун"""
    def __init__(self):
        self._memento = None

    def get_memento(self):
        return self._memento

    def set_memento(self, memento):
        self._memento = memento


class Originator(object):
    """Создатель"""
    def __init__(self):
        self._state = None

    def set_state(self, state):
        self._state = state

    def get_state(self):
        return self._state

    def save_state(self):
        return Memento(self._state)

    def restore_state(self, memento):
        self._state = memento.get_state()


originator = Originator()
caretaker = Caretaker()

originator.set_state('on')
print ('Originator state:', originator.get_state())  # Originator state: on
caretaker.set_memento(originator.save_state())

originator.set_state('off')
print ('Originator change state:', originator.get_state()) # Originator change state: off

originator.restore_state(caretaker.get_memento())
print ('Originator restore state:', originator.get_state()) # Originator restore state: on

"""
Наблюдатель (Observer, Dependents, Publish-Subscribe) - паттерн поведения объектов.

Определяет зависимость типа "один ко многим" между объектами таким образом,
что при изменении состояния одного объекта все зависящие от него оповещаются об этом
и автоматически обновляются.
"""


class Subject(object):
    """Субъект"""
    def __init__(self):
        self._data = None
        self._observers = set()

    def attach(self, observer):
        # подписаться на оповещение
        if not isinstance(observer, ObserverBase):
            raise TypeError()
        self._observers.add(observer)

    def detach(self, observer):
        # отписаться от оповещения
        self._observers.remove(observer)

    def get_data(self):
        return self._data

    def set_data(self, data):
        self._data = data
        self.notify(data)

    def notify(self, data):
        # уведомить всех наблюдателей о событии
        for observer in self._observers:
            observer.update(data)


class ObserverBase(object):
    """Абстрактный наблюдатель"""
    def update(self, data):
        raise NotImplementedError()


class Observer(ObserverBase):
    """Наблюдатель"""
    def __init__(self, name):
        self._name = name

    def update(self, data):
        print ('%s: %s' % (self._name, data))


subject = Subject()
subject.attach(Observer('Наблюдатель 1'))
subject.attach(Observer('Наблюдатель 2'))
subject.set_data('данные для наблюдателя')
# Наблюдатель 2: данные для наблюдателя
# Наблюдатель 1: данные для наблюдателя

"""
Состояние (State) - паттерн поведения объектов.

Позволяет объекту варьировать свое поведение в зависимости от внутреннего состояния.
Извне создается впечатление, что изменился класс объекта.
"""


class LampStateBase(object):
    """Состояние лампы"""
    def get_color(self):
        raise NotImplementedError()


class GreenLampState(LampStateBase):
    def get_color(self):
        return 'Green'


class RedLampState(LampStateBase):
    def get_color(self):
        return 'Red'


class BlueLampState(LampStateBase):
    def get_color(self):
        return 'Blue'


class Lamp(object):
    def __init__(self):
        self._current_state = None
        self._states = self.get_states()

    def get_states(self):
        return [GreenLampState(), RedLampState(), BlueLampState()]

    def next_state(self):
        if self._current_state is None:
            self._current_state = self._states[0]
        else:
            index = self._states.index(self._current_state)
            if index < len(self._states) - 1:
                index += 1
            else:
                index = 0
            self._current_state = self._states[index]
        return self._current_state

    def light(self):
        state = self.next_state()
        print (state.get_color())


lamp = Lamp()
[lamp.light() for i in range(3)]
# Green
# Red
# Blue
[lamp.light() for i in range(3)]
# Green
# Red
# Blue


"""
Строитель (Builder) - паттерн, порождающий объекты.

Отделяет конструирование сложного объекта от его представления,
так что в результате одного и того же процесса конструирования могут получаться разные представления.

От абстрактной фабрики отличается тем, что делает акцент на пошаговом конструировании объекта.
Строитель возвращает объект на последнем шаге, тогда как абстрактная фабрика возвращает объект немедленно.

Строитель часто используется для создания паттерна компоновщик.
"""


class Builder(object):
    def build_body(self):
        raise NotImplementedError()

    def build_lamp(self):
        raise NotImplementedError()

    def build_battery(self):
        raise NotImplementedError()

    def create_flashlight(self):
        raise NotImplementedError()


class Flashlight(object):
    """Карманный фонарик"""
    def __init__(self, body, lamp, battery):
        self._shine = False  # излучать свет
        self._body = body
        self._lamp = lamp
        self._battery = battery

    def on(self):
        self._shine = True

    def off(self):
        self._shine = False

    def __str__(self):
        shine = 'on' if self._shine else 'off'
        return 'Flashlight [%s]' % shine


class Lamp(object):
    """Лампочка"""


class Body(object):
    """Корпус"""


class Battery(object):
    """Батарея"""


class FlashlightBuilder(Builder):
    def build_body(self):
        return Body()

    def build_battery(self):
        return Battery()

    def build_lamp(self):
        return Lamp()

    def create_flashlight(self):
        body = self.build_body()
        lamp = self.build_lamp()
        battery = self.build_battery()
        return Flashlight(body, lamp, battery)


builder = FlashlightBuilder()
flashlight = builder.create_flashlight()
flashlight.on()
print(flashlight) # Flashlight [on]

"""
Фабричный метод (Factory Method) - паттерн, порождающий классы.

Определяет интерфейс для создания объекта, но оставляет подклассам решение о том, какой класс инстанцировать.
Позволяет делегировать инстанцирование подклассам.

Абстрактная фабрика часто реализуется с помощью фабричных методов.
Фабричные методы часто вызываются внутри шаблонных методов.
"""


class Document(object):
    def show(self):
        raise NotImplementedError()


class ODFDocument(Document):
    def show(self):
        print ('Open document format')


class MSOfficeDocument(Document):
    def show(self):
        print ('MS Office document format')


class Application(object):
    def create_document(self, type_):
        # параметризованный фабричный метод `create_document`
        raise NotImplementedError()


class MyApplication(Application):
    def create_document(self, type_):
        if type_ == 'odf':
            return ODFDocument()
        elif type_ == 'doc':
            return MSOfficeDocument()
        else:
            return Document()


app = MyApplication()
app.create_document('odf').show()  # Open document format
app.create_document('doc').show()  # MS Office document format
try:
    app.create_document('pdf').show()
except:
    print("NotImplementedError")

"""
Прототип - паттерн, порождающий объекты.

Задает виды создаваемых объектов с помощью экземпляра-прототипа
и создает новые объекты путем копирования этого прототипа.
"""

import copy


class Prototype(object):
    def __init__(self):
        self._objects = {}

    def register(self, name, obj):
        self._objects[name] = obj

    def unregister(self, name):
        del self._objects[name]

    def clone(self, name, attrs):
        obj = copy.deepcopy(self._objects[name])
        obj.__dict__.update(attrs)
        return obj


class Bird(object):
    """Птица"""


prototype = Prototype()
prototype.register('bird', Bird())

owl = prototype.clone('bird', {'name': 'Owl'})
print (type(owl), owl.name ) # <class '__main__.Bird'> Owl

duck = prototype.clone('bird', {'name': 'Duck'})
print (type(duck), duck.name)  # <class '__main__.Bird'> Duck

"""
Одиночка (Singleton) - паттерн, порождающий объекты.

Гарантирует, что у класса есть только один экземпляр, и предоставляет к нему глобальную точку доступа.

С помощью паттерна одиночка могут быть реализованы многие паттерны (абстрактная фабрика, строитель, прототип).
"""


class SingletonMeta(type):
    def __init__(cls, *args, **kwargs):
        cls._instance = None
        # глобальная точка доступа `Singleton.get_instance()`
        cls.get_instance = classmethod(lambda c: c._instance)
        super(SingletonMeta, cls).__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instance


class Singleton(object):
    __metaclass__ = SingletonMeta

    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name


obj1 = Singleton('MyInstance 1')
print (obj1.get_name())  # MyInstance 1

obj2 = Singleton('MyInstance 2')
print (obj2.get_name() ) # MyInstance 1

print (obj1 is obj2 is Singleton.get_instance() ) # True

"""
Адаптер - паттерн, структурирующий классы и объекты.

Преобразует интерфейс одного класса в интерфейс другого, который ожидают клиенты.
Адаптер обеспечивает совместную работу классов с несовместимыми интерфейсами, которая без него была бы невозможна.
"""


class Dog(object):
    def __init__(self, name):
        self._name = name

    def bark(self):
        return '%s: гав-гав!' % self._name


class Cat(object):
    def __init__(self, name):
        self._name = name

    def meow(self):
        return '%s: мяу-мяу!' % self._name


class CatAdapter(Dog):
    # благодаря адаптеру мы можем использовать
    # интерфейс класса `Dog`, а реализацию класса `Cat`.

    def __init__(self, name):
        super(CatAdapter, self).__init__(name=name)
        self._cat = Cat(name=name)

    def bark(self):
        # запрос `bark` преобразуется в запрос `meow`
        return self._cat.meow()


dog = Dog('Тузик')
print (dog.bark())  # Тузик: гав-гав!

dog = CatAdapter('Тузик')
print (dog.bark())  # Тузик: мяу-мяу!

"""
Фасад (Facade) - паттерн, структурирующий объекты.

Предоставляет унифицированный интерфейс вместо набора интерфейсов некоторой подсистемы.
Фасад определяет интерфейс более высокого уровня, который упрощает использование подсистемы.
"""


class Paper(object):
    """Бумага"""
    def __init__(self, count):
        self._count = count

    def get_count(self):
        return self._count

    def draw(self, text):
        if self._count > 0:
            self._count -= 1
            print (text)


class Printer(object):
    """Принтер"""
    def error(self, msg):
        print ('Ошибка: %s' % msg)

    def print_(self, paper, text):
        if paper.get_count() > 0:
            paper.draw(text)
        else:
            self.error('Бумага закончилась')


class Facade(object):
    def __init__(self):
        self._printer = Printer()
        self._paper = Paper(1)

    def write(self, text):
        self._printer.print_(self._paper, text)


f = Facade()
f.write('Hello world!')  # Hello world!
f.write('Hello world!')  # Ошибка: Бумага закончилась

"""
Заместитель (Proxy, Surrogate) - паттерн, структурирующий объекты.

Является суррогатом другого объекта и контролирует доступ к нему.
"""


from functools import partial


class ImageBase(object):
    """Абстрактное изображение"""
    @classmethod
    def create(cls, width, height):
        """Создает изображение"""
        return cls(width, height)

    def draw(self, x, y, color):
        """Рисует точку заданным цветом"""
        raise NotImplementedError()

    def fill(self, color):
        """Заливка цветом"""
        raise NotImplementedError()

    def save(self, filename):
        """Сохраняет изображение в файл"""
        raise NotImplementedError()


class Image(ImageBase):
    """Изображение"""
    def __init__(self, width, height):
        self._width = int(width)
        self._height = int(height)

    def draw(self, x, y, color):
        print ('Рисуем точку; координаты: (%d, %d); цвет: %s' % (x, y, color))

    def fill(self, color):
        print ('Заливка цветом %s' % color)

    def save(self, filename):
        print ('Сохраняем изображение в файл %s' % filename)


class ImageProxy(ImageBase):
    """
    Заместитель изображения.
    Откладывает выполнение операций над изображением до момента его сохранения.
    """
    def __init__(self, *args, **kwargs):
        self._image = Image(*args, **kwargs)
        self.operations = []

    def draw(self, *args):
        func = partial(self._image.draw, *args)
        self.operations.append(func)

    def fill(self, *args):
        func = partial(self._image.fill, *args)
        self.operations.append(func)

    def save(self, filename):
        # выполняем все операции над изображением
        map(lambda f: f(), self.operations)
        # сохраняем изображение
        self._image.save(filename)


img = ImageProxy(200, 200)
img.fill('gray')
img.draw(0, 0, 'green')
img.draw(0, 1, 'green')
img.draw(1, 0, 'green')
img.draw(1, 1, 'green')
img.save('image.png')

# Заливка цветом gray
# Рисуем точку; координаты: (0, 0); цвет: green
# Рисуем точку; координаты: (0, 1); цвет: green
# Рисуем точку; координаты: (1, 0); цвет: green
# Рисуем точку; координаты: (1, 1); цвет: green
# Сохраняем изображение в файл image.png