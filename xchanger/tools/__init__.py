# -*- coding:utf-8 -*-
import logging
import sys

__author__ = 'pavel.sh'


# Главная функция программы
def main():
    pass

# Точка входа в главную функцию
if __name__ == '__main__':
    # Режим логирования
    logging.basicConfig(filename='ymbet.log', level=logging.DEBUG, format='%(asctime)s %(name)s > %(message)s')
    main()
    # Завершение работы
    sys.exit()