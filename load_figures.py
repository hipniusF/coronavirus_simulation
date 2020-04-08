import pylab
import pandas


def open_figure(i, figure, infected_pop=True, healthy_pop=True, dead_pop=True, cure_pop=True, title=''):
    pylab.figure(figure)
    data = pandas.read_csv(f'figures/Figure_{i}.csv')

    x_vals = range(len(data))

    if infected_pop:
        pylab.plot(x_vals, data.Infect, label=f'Infected_{i}')

    if healthy_pop:
        pylab.plot(x_vals, data.Healthy, label=f'Healthy_{i}')

    if dead_pop:
        pylab.plot(x_vals, data.Dead, label=f'Dead_{i}')

    if cure_pop:
        pylab.plot(x_vals, data.Cure, '--', label=f'Cure_{i}')

    pylab.legend()
    pylab.xlabel('Number of the days')
    pylab.ylabel('Number of people')
    pylab.title(title)


if __name__ == "__main__":

    index = input('Enter figures index: ')
    show_infected_pop = True if input(
        'Show Infected population? (true/false): ') == 'true' else False

    show_healthy_pop = True if input(
        'Show Healthy population? (true/false): ') == 'true' else False

    show_dead_pop = True if input(
        'Show Dead population? (true/false): ') == 'true' else False

    show_cure_pop = True if input(
        'Show Cure population? (true/false): ') == 'true' else False

    open_figure(int(index), int(index), show_infected_pop,
                show_healthy_pop, show_dead_pop, show_cure_pop)

    pylab.show()
