
from comp import *
import tkinter as tk
from tkinter import ttk
import os
import numpy as np
import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt


class Signal():
    def __init__(self, data):
        self.data = data
        self.Signal1 = np.array([data[0]])
        print(self.Signal1.shape)
        self.Signal2 = np.array([data[1]])
        print(self.Signal2.shape)

    def Process(self):
        # Сравниваем размеры сигналов
        try:
            if self.Signal1.shape[1] != self.Signal2.shape[1]:
                raise Exception('Размеры сигналов не совпадают')
        except Exception as inst:
            print(inst)

        n = self.Signal1.shape[1]

        # Создаем аподизирующий фильтр Блекмена-Харриса
        blackman_harris = [0.3635819, 0.4891775, 0.1365995, 0.0106411]
        x = np.arange(1, n + 1)
        A = blackman_harris[0] \
            - blackman_harris[1] * np.cos(x * 2 * np.pi / n) \
            + blackman_harris[2] * np.cos(x * 4 * np.pi / n) \
            - blackman_harris[3] * np.cos(x * 6 * np.pi / n)
        # print("A:  ", A)
        # print(A.shape)
        # plt.plot(x, A)
        # plt.show()

        # Вычитание срееднего и апподизачия  сигнала
        self.Averaged1 = (self.Signal1 - np.mean(self.Signal1)) * A
        self.Averaged2 = (self.Signal2 - np.mean(self.Signal2)) * A

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

        self.Filter1 = 1. / (1 + np.power(((np.arange(1, sh1 + 1) - w1m) / wc), (2 * k)))
        self.Filter2 = 1. / (1 + np.power(((np.arange(1, sh2 + 1) - w2m) / wc), (2 * k)))

        # print("Filter1:  ",Filter1[ :10])
        # print(Filter1.shape)
        # print("Filter2:  ",Filter2[ :10])
        # print(Filter2.shape)

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
        self.Process()
        ind1 = int(np.round(self.Phase.shape[1] * 0.2)) - 1
        ind2 = int(np.round(self.Phase.shape[1] - (self.Phase.shape[1] * 0.2)))
        self.Phi = np.mean(self.Phase[0, ind1: ind2])
        print("Phi", self.Phi * 180 / np.pi)
        return self.Phi

def Compute_Phase(s1, s2):
    sh1 = np.array(s1.data).shape[1]
    sh2 = np.array(s2.data).shape[1]

    # Phase1 = np.zeros((1, sh1))
    #
    # Phase2 = np.zeros((1, sh2))
    # Phi1 = np.zeros((1, sh1))
    # Phi2 = np.zeros((1, sh2))

    Phi1 = s1.Get_Phase()
    print(Phi1)
    # Phase1, sp11, sp12 = Process(np.array([s1.data[0]]), np.array([s1.data[1]]))

    # ind1 = int(np.round(Phase1.shape[1] * 0.2)) - 1
    # ind2 = int(np.round(Phase1.shape[1] - (Phase1.shape[1] * 0.2)))

    # print("ind1_1: ", ind1)
    # print("ind1_2: ", ind2)

    # Phi1 = np.mean(Phase1[0, ind1: ind2])
    # print("Phi1", Phi1 * 180 / np.pi)

    # Phase2, sp21, sp22 = Process(np.array([s2[0]]), np.array([s2[1]]))
    Phi2 = s2.Get_Phase()
    # ind1 = int(np.round(Phase2.shape[1] * 0.2)) - 1
    # ind2 = int(np.round(Phase2.shape[1] - (Phase2.shape[1] * 0.2)))

    # print("ind2_1: ", ind1)
    # print("ind2_2: ", ind2)

    # Phi2 = np.mean(Phase2[0, ind1: ind2])
    # print("Phi2", Phi2 * 180 / np.pi)
    # print("phi1: ", Phi1)
    # print("phi2: ", Phi2)

    DeltaPhi = (np.mean(Phi2) - np.mean(Phi1)) / 2
    #
    # print("mean_phi1: ", np.mean(Phi1))
    # print("mean_phi2: ", np.mean(Phi2))

    print(DeltaPhi * 180 / np.pi)
    # return DeltaPhi, Phase1, Phase2, sp11, sp21
    return DeltaPhi




def test():
    # with open("test.LAn10", "rb") as f:
    #     byte = f.read(1)
    #     while byte != b"":
    #         v = int(byte, 2)
    #         print(v)

    # infile = open('test.LAn10', 'rb')
    # for chunk in read_in_chunks(infile):
    #     print(chunk)

    File_PathName1 = ["2023_03_16_101.LAn10"]
    File_PathName2 = ["2023_03_16_110.LAn10"]

    f = np.fromfile("2023_09_27__02_01.003.LAn10", dtype='uint16', offset=4)
    f1 = np.zeros((2, int(f.shape[0] / 2)))
    f1[0] = f[::2]
    f1[1] = f[1::2]
    print(f.shape)
    print(f)
    f = np.fromfile("2023_09_27__02_00.003.LAn10", dtype='uint16', offset=4)
    f2 = np.zeros((2, int(f.shape[0] / 2)))
    f2[0] = f[::2]
    f2[1] = f[1::2]

    Compute_Phase(f1, f2)

    # n = 100000
    # x = np.arange(n)
    # plt.plot(x,f1[0,:n])
    # plt.plot(x,f1[1])
    # plt.show()
    #
    # a = np.zeros((5,10))+2
    # b = np.zeros((5,10))+3
    #
    # z = np.vstack((np.array([a]),np.array([b])))
    # print(z.shape)
    # print(z)

    # print("Myread11  ", f1[0].shape)
    # print(f1[0,:10])
    # print("Myread12  ", f1[1].shape)
    # print(f1[1,:10])
    # print("Myread21  ", f2[0].shape)
    # print(f2[0, :10])
    # print("Myread22  ", f2[1].shape)
    # print(f2[1, :10])
