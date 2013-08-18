#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# Copyright (c) 2011-2013 Fatih Bostancı <faopera@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  

# bağımlılıklar: python 3, python-dbus

# TODO: qt (ve ? gtk) arayüz
# TODO: kapatma başlamadan ekrana işlemi iptal etme penceresi
# TODO: dbus python 3 e geçince uygulamayı python3 e taşıma.

import getopt, sys
from dbus import SystemBus,Interface
from sys import exit,argv,stdout
from time import strftime,sleep


def bekleme_goster(bekleme_suresi):
    try:
        bekleme_suresi -= 1

        while bekleme_suresi > 0:
            print("\033[;1mBilgisayarınız \033[1;33;44m",int(bekleme_suresi / 3600), "saat", \
                  int(bekleme_suresi % 3600 / 60), "dakika", int(bekleme_suresi % 60), "saniye", \
                  "\033[;1m sonra kapatılacak...\033[0m",end="\r")
           # sys.stdout.flush()
            bekleme_suresi -= 1
            sleep(1)
    except KeyboardInterrupt:
        print("\n\033[1;41mKullanıcı tarafından işlem iptal edildi !!!\033[0m")
        exit(1)

def simdi_kapat(istek):
    bus = SystemBus()
    dbus_k = bus.get_object('org.freedesktop.ConsoleKit',
                            '/org/freedesktop/ConsoleKit/Manager')
    dbus_kapat = Interface(dbus_k, 'org.freedesktop.ConsoleKit.Manager')

    if istek == 'Stop':
        print("\033[1;41mBilgisayarınız kapatılıyor...\033[0m")
        dbus_kapat.Stop()
    else:
        print("\033[1;41mBilgisayarınız yeniden başlatılıyor...\033[0m")
        dbus_kapat.Restart()

#def simdi_askiya_al(istek):
#    bus = SystemBus()
#    dbus_as = bus.get_object('org.freedesktop.UPower',
#                            '/org/freedesktop/UPower')
#    dbus_askiya_al = Interface(dbus_as, 'org.freedesktop.UPower')
#    dbus_askiya_al.Suspend()

class PyKapat:
    def main(self):
        try:
            opts, args = getopt.gnu_getopt(sys.argv[1:], "hvkys:d:",
                        ["help", "version", "kapat", "yeniden-baslat", "saat=", "dakika="])
        except getopt.GetoptError as err:
            print("pykapat: %s" % (str(err)))
            exit(2)

        for o, a in opts:
            if o in ("-k", "--kapat"):
                simdi_kapat("Stop")
            elif o in ("-y", "--yeniden-baslat"):
                simdi_kapat("Restart")
            elif o in ("-s", "--saat"):
                kapat.su_saatte(a)
            elif o in ("-d", "--dakika"):
                kapat.dakika_sonra(a)
            elif o in ("-v", "--version"):
                kapat.surum_bilgisi()
            elif o in ("-h", "--help"):
                kapat.kullanim()
            else:
                assert False, "Yakalanamayan seçenek"


    def dakika_sonra(self, dakika):
        try:
            self.dakika = int(dakika)
        except ValueError:
            print("\033[1;41mDakika olarak sayısal bir değer giriniz.\033[0m")
            exit(1)

        if int(self.dakika) < 0:
            print("\033[1;41mGirilen dakika 0'dan küçük olamaz.\033[0m")
            exit(1)

        self.dakika_bekleme_suresi = int(self.dakika) * 60
        bekleme_goster(self.dakika_bekleme_suresi)
        simdi_kapat("Stop")

    def su_saatte(self, saat):
        self.saat = saat
        saat_ayir = self.saat.split(":", 1)

        try:
            int(saat_ayir[0])
            int(saat_ayir[1])

        except ValueError:
            print("\033[1;41mSaat olarak sayısal bir değer giriniz.\033[0m")
            exit(1)

        except IndexError:
            print("\033[1;41mSaat ve dakika arasında ':' olmalı.\033[0m")
            exit(1)

        if int(saat_ayir[0]) > 23:
            print("\033[1;41mGirilen saat en fazla 23 olabilir.\033[0m")
            exit(1)

        elif int(saat_ayir[0]) < 0:
            print("\033[1;41mGirilen saat 0'dan küçük olamaz.\033[0m")
            exit(1)

        if int(saat_ayir[1]) > 59:
            print("\033[1;41mGirilen dakika en fazla 59 olabilir.\033[0m")
            exit(1)

        elif int(saat_ayir[1]) < 0:
            print("\033[1;41mGirilen dakika 0'dan küçük olamaz.\033[0m")
            exit(1)


        self.girilen_saat_saniye = int(saat_ayir[0]) * 3600 + int(saat_ayir[1]) * 60
        self.simdiki_saat_saniye = int(strftime('%H')) * 3600 + int(strftime('%M')) * 60 + int(strftime('%S'))

        if self.girilen_saat_saniye >= self.simdiki_saat_saniye:
            self.saat_bekleme_suresi = self.girilen_saat_saniye - self.simdiki_saat_saniye
            print("\033[1;1mBilgisayarınızın kapatılacağı saat:\033[1;33m %s\033[0m" % (self.saat) )
            bekleme_goster(self.saat_bekleme_suresi)
            simdi_kapat('Stop')

        elif self.girilen_saat_saniye < self.simdiki_saat_saniye:
            self.saat_bekleme_suresi = 24 * 3600 - self.simdiki_saat_saniye + self.girilen_saat_saniye
            print("\033[1;1mBilgisayarınızın kapatılacağı saat:\033[1;33m %s (Yarın)\033[0m" % (self.saat))
            bekleme_goster(self.saat_bekleme_suresi)
            simdi_kapat('Stop')

    def surum_bilgisi(self):
        print("PyKapat v0.3.0")

    def kullanim(self):
        print("""
        -s, --saat <ss:dd>       : Girilen saatte bilgisayarı kapatır.
        -d, --dakika <dakika>    : Girilen dakika sonra bilgisayarı kapatır.
        -k, --kapat              : Bilgisayarı hemen kapatır.
        -y, --yeniden-baslat     : Bilgisayarı hemen yeniden başlatır.
        -v, --version            : Uygulamanın sürümünü görüntüler.
        -h, --help               : Bu yardım çıktısını görüntüler.
        """)

kapat = PyKapat()

if __name__ == "__main__":
    kapat.main()


###Sürüm Geçmişi Başlangıç###
#
# v0.3.0
# * Python 3'e taşınma
#
#------------------------------------------------
# v0.2.0
# * Renkli çıktılar
# * Terminalde geri sayım sayacı (saat,dakika,saniye olarak) gösterme
#
#------------------------------------------------
# v0.1.1
# * KeyboardInterrupt ve Index Error yakalama
#
#------------------------------------------------
# v0.1.0
#* ilk sürüm.
#
###Sürüm Geçmişi Son###

#vim: set ts=4 sw=4 et:
