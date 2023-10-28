import numpy as np


class Signal():
    '''
    Класс для сохранения данных и расчетов
    '''
    def __init__(self, data):
        '''
        Конструктор класса
        :param data: данные файла в виде numpy array
        '''
        self.data = data
        self.Signal1 = np.array([data[0]])
        self.Signal2 = np.array([data[1]])
        self.filopt = None

    def Setfilter(self,filopt):
        '''
        Настройка фильтра
        :param filopt: Тип фильтра
        '''

        n = self.Signal1.shape[1]
        if filopt == "Прямоугольное окно":
            self.A = 1
        elif filopt == "Треугольное окно Бартлетта":
            self.A = (n - 2 * np.abs(np.arange(1,n+1) - n/2)) / n
        elif filopt == "Синус окнo":
            self.A = np.sin(np.arange(1,n+1) * np.pi/n)
        elif filopt == "Oкно Ханна":
            self.A = 0.5 * (1-np.cos(np.arange(1,n+1) * 2 * np.pi/n))
        elif filopt == "Окно Хемминга":
            self.A = 0.54 - 0.46*np.cos(np.arange(1,n+1) * 2 * np.pi/n)
        elif filopt == "Окно Блекмена-Харриса":
            blackman_harris = [0.3635819, 0.4891775, 0.1365995, 0.0106411]
            x = np.arange(1, n + 1)
            self.A = blackman_harris[0] \
                - blackman_harris[1] * np.cos(x * 2 * np.pi / n) \
                + blackman_harris[2] * np.cos(x * 4 * np.pi / n) \
                - blackman_harris[3] * np.cos(x * 6 * np.pi / n)
        elif filopt == "Окно Наталла":
            blackman_harris = [0.355768, 0.487396, 0.144232, 0.012604]
            x = np.arange(1, n + 1)
            self.A = blackman_harris[0] \
                - blackman_harris[1] * np.cos(x * 2 * np.pi / n) \
                + blackman_harris[2] * np.cos(x * 4 * np.pi / n) \
                + blackman_harris[3] * np.cos(x * 6 * np.pi / n)
        else:
            raise Exception("Wrong value passed to filter")


    def Process(self):
        '''
        Обработка данных
        Вычисление спектра, применение фильтра, расчет фазы
        '''

        # Сравниваем размеры сигналов
        try:
            if self.Signal1.shape[1] != self.Signal2.shape[1]:
                raise Exception('Размеры сигналов не совпадают')
        except Exception as inst:
            print(inst)

        n = self.Signal1.shape[1]


        # print("A:  ", A)
        # print(A.shape)
        # plt.plot(x, A)
        # plt.show()

        # Вычитание срееднего и апподизачия  сигнала
        self.Averaged1 = (self.Signal1 - np.mean(self.Signal1)) * self.A
        self.Averaged2 = (self.Signal2 - np.mean(self.Signal2)) * self.A

        # print(Averaged1[0,:10])
        # print(Averaged1.shape)
        # print(Averaged2[0,:10])
        # print(Averaged2.shape)

        # Вычисление спектра
        self.Spectrum1 = np.fft.fftshift(np.fft.fft(self.Averaged1))
        self.Spectrum2 = np.fft.fftshift(np.fft.fft(self.Averaged2))

        # print(Spectrum1[0, :10])
        # print(Spectrum1.shape)
        # print(Spectrum2[0,:10])
        # print(Spectrum2.shape)

        # Вычисляем максимум первого порядка
        self.SpectrumHPF1 = np.copy(self.Spectrum1)
        self.SpectrumHPF2 = np.copy(self.Spectrum2)

        self.SpectrumHPF1[0, 0: int(np.floor(n / 2) + 1)] = 0
        self.SpectrumHPF2[0, 0: int(np.floor(n / 2) + 1)] = 0

        # print(int(np.floor(n / 2) + 1))

        # print(SpectrumHPF1[0, :10])
        # print(SpectrumHPF1.shape)
        # print(SpectrumHPF2[0, :10])
        # print(SpectrumHPF2.shape)

        w1m = np.argmax(self.SpectrumHPF1)
        w2m = np.argmax(self.SpectrumHPF2)

        # print(w1m)
        # print(w2m)

        # Создаем фильтр Баттерворта
        k = 5  # Порядок фильтра

        # Размеры Spectrum1,2
        sh1, sh2 = self.Spectrum1.shape[1], self.Spectrum2.shape[1]

        # Определяем ширину фильтра
        if np.floor(0.1 * (w1m - (np.floor(sh1 / 2)))) > 5:
            wc = int(np.floor(0.1 * (w1m - (np.floor(sh1 / 2)))))
        else:
            wc = 5

        # print("cond  ", np.floor(0.1 * (w1m - (np.floor(sh1 / 2)))))
        # print(wc)

        self.Filter1 = 1. / np.sqrt((1 + np.power(((np.arange(1, sh1 + 1) - w1m) / wc), (2 * k))))
        self.Filter2 = 1. / np.sqrt((1 + np.power(((np.arange(1, sh2 + 1) - w2m) / wc), (2 * k))))

        # print("Filter1:  ",self.Filter1[ :10])
        # print(self.Filter1.shape)
        # print("Filter2:  ",self.Filter2[ :10])
        # print(self.Filter2.shape)

        # Наложение фльтра и вычисление обратного преобразования
        self.SignalFiltered1 = np.fft.ifft(np.fft.fftshift(self.Spectrum1[0] * self.Filter1))
        self.SignalFiltered2 = np.fft.ifft(np.fft.fftshift(self.Spectrum2[0] * self.Filter2))

        # print(SignalFiltered1[:10])
        # print(SignalFiltered1.shape)
        # print(SignalFiltered2[:10])
        # print(SignalFiltered1.shape)

        # Определение фазы
        self.Phase = np.angle(self.SignalFiltered2 * np.conjugate(self.SignalFiltered1))
        self.Phase = np.array([self.Phase])
        # print("Phase  ", np.array([Phase]))
        # print(np.array([Phase]).shape)

        # return np.array([self.Angle])
        # return np.array([Phase]), np.absolute(Spectrum1), np.absolute(Spectrum2)

    def Get_Phase(self):
        '''
        Считает фазу сигнала
        '''

        self.Process()
        ind1 = int(np.round(self.Phase.shape[1] * 0.2)) - 1
        ind2 = int(np.round(self.Phase.shape[1] - (self.Phase.shape[1] * 0.2)))
        self.Phi = np.mean(self.Phase[0, ind1: ind2])
        print("Phi", self.Phi * 180 / np.pi)
        return self.Phi

def Compute_Phase(s1, s2):
    '''
    Считает разницу фаз двух сигналов
    :param s1: Первый файл
    :param s2: Второй файл
    '''

    Phi1 = s1.Get_Phase()
    Phi2 = s2.Get_Phase()

    DeltaPhi = (np.mean(Phi2) - np.mean(Phi1)) / 2
    print(DeltaPhi * 180 / np.pi)
    return DeltaPhi

