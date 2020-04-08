import pylab


def calc_avg_at_day(infect_pop, day):
    data_through_days = [n[day] for n in infect_pop]

    return sum(data_through_days) / len(data_through_days)


def save_i(i):
    f = open(f'fix/{i}.txt')
    infect_pop = [[], [], [], [], []]

    for line in f:
        try:
            data = line.strip().split(' ')
            infect_pop[int(data[0])].append(int(data[2]))
        except IndexError:
            pass

    x_vals = range(1, len(infect_pop[0]))
    y_vals = [calc_avg_at_day(infect_pop, day) for day in x_vals]

    pylab.figure(i)
    pylab.plot(x_vals, y_vals, label='Infected')
    pylab.legend()
    pylab.xlabel('Number of the day')
    pylab.ylabel('Number of infected')
    pylab.savefig(f'figures/Figure_{i}')

    fA = open(f'figures/Figure_{i}_a.txt', 'w+')
    fB = open(f'figures/Figure_{i}_b.txt', 'w+')

    for y in y_vals:
        fA.write(f'{y}\n')

    fA.close()


index = input('Enter figures index (or "all" for all of them): ')

if index == 'all':
    num_figures = int(input('Enter number of figures: ')) + 1
    for i in range(1, num_figures):
        save_i(i)

else:
    save_i(int(index))

########## WARNING ##########
#   ESTE PROGRAMA DE FIXEAD ESTÁ ESCRITO PARA EL CASO DE 5 TRIALS #
#   PARA CUALQUIER OTRO NÚMERO DE TRIALS DE DEBERÁ EDITAR EL NÚMERO #
#   DE LISTAS VACIAS EN LA LÍNEA 12


# RECUERDA TAMBIÉN AÑADIR A MANO LOS DATOS DE figures.txt
