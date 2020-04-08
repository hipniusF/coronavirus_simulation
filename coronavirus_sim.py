import random
import numpy
import pylab
import pandas


class Person():
    def __init__(self, infected, death_prob, cure_prob, inf_prob, on_risk, days_before_cure):
        """
        Arg:
        -infected (bool): tells if the Person is infected of coronavirus
        -death_prob (float in [0, 1]): tells the probability of a person to die each day
        -inf_prob (float in [0, 1]): probability of infecting another person per day
        -on_quarantine (bool): True if the person is in quarantine
        -days_infected (int): number of days passed since infection
        """

        self.infected = infected
        self.death_prob = death_prob
        self.cure_prob = cure_prob
        self.inf_prob = inf_prob
        self.on_quarantine = False
        self.days_infected = 0
        self.on_risk = on_risk
        self.days_before_cure = days_before_cure

    def set_on_quarantine(self):
        self.on_quarantine = True

    def set_infected(self):
        self.infected = True

    def cure(self):
        self.infected = False

    def infection_advances(self):
        if self.on_risk:
            if random.random() < self.death_prob * 10:
                return -1
        else:
            if random.random() < self.death_prob:
                return -1

        if (self.days_infected > self.days_before_cure and random.random() < self.cure_prob):
            return 1

        return 0

    def infection(self):
        """
        Return True with a self.inf_prob probability if not self.quarantine. An with self.in_prob / 4 otherwise.
        """

        if not self.on_quarantine:
            return random.random() < self.inf_prob
        else:
            return random.random() < self.inf_prob / 2


class Country():
    def __init__(self, healthy_pop, infect_pop):
        """
        Arg:
        -healthy_pop (list) = list of Person() instances with "infected" attribute to false
        -infected_pop (list) = list of Person() instances with "infected" attribute to true

        1- the infected people infects a healthy person with a probability of their inf_prob
        2- each enfected person (not including the new infected) decides whenever it dies (with death_prob probability),
           it's cured (with cure_prob) or notting happends (remaining cases)
        """

        self.healthy_pop = healthy_pop
        self.infect_pop = infect_pop
        self.dead_pop = []
        self.cure_pop = []

    def activate_quarantine(self, qurant_prob):
        for person in self.healthy_pop:
            if random.random() < qurant_prob:
                person.set_on_quarantine()

        for person in self.infect_pop:
            if random.random() < qurant_prob:
                person.set_on_quarantine()

    def get_infected_num(self):
        return len(self.infect_pop)

    def get_healthy_num(self):
        return len(self.healthy_pop)

    def get_dead_num(self):
        return len(self.dead_pop)

    def get_cure_num(self):
        return len(self.cure_pop)

    def pass_day(self):
        new_healthy_pop = self.healthy_pop
        new_infect_pop = self.infect_pop

        for person in self.infect_pop:
            person.days_infected += 1
            # New infected for today
            if person.infection():
                try:
                    new_infected = self.healthy_pop[random.randint(
                        0, len(self.healthy_pop))]
                    new_infected.set_infected()

                    new_healthy_pop.remove(new_infected)
                    new_infect_pop.append(new_infected)
                except IndexError:
                    pass

            # Cure, pass or death
            state_after_day = person.infection_advances()

            if state_after_day == 1:
                person.cure()
                new_infect_pop.remove(person)
                new_healthy_pop.append(person)
                self.cure_pop.append(person)

            elif state_after_day == -1:
                new_infect_pop.remove(person)
                self.dead_pop.append(person)

        self.healthy_pop = new_healthy_pop
        self.infect_pop = new_infect_pop

        return new_healthy_pop, new_infect_pop


def calc_avg_at_day(infect_pop, day):
    data_through_days = [n[day] for n in infect_pop]

    return sum(data_through_days) / len(data_through_days)


def calc_std(infect_pop, day):
    mean = calc_avg_at_day(infect_pop, day)
    pop_at_day = [data[day] for data in infect_pop]

    std = (sum([(x - mean) ** 2 for x in pop_at_day]) / len(infect_pop)) ** 0.5
    return mean, std


def sim_virus(index, init_healthy, init_infected, death_prob, cure_prob, inf_prob, on_risk_ratio, days_before_cure, num_trials, days_to_check, to_print=False, start_of_quarantine=None):
    num_on_risk = int((on_risk_ratio / 100) * init_healthy)

    infect_pops = [''] * num_trials
    healthy_pops = [''] * num_trials
    dead_pops = [''] * num_trials
    cure_pops = [''] * num_trials

    for trial in range(num_trials):
        infect_pops[trial] = [''] * (days_to_check + 1)
        healthy_pops[trial] = [''] * (days_to_check + 1)
        dead_pops[trial] = [''] * (days_to_check + 1)
        cure_pops[trial] = [''] * (days_to_check + 1)

        healthy_pop = []
        infect_pop = []

        for i in range(init_healthy):
            healthy_pop.append(
                Person(False, death_prob, cure_prob, inf_prob, True if i < num_on_risk else False, days_before_cure))

        for i in range(init_infected):
            infect_pop.append(
                Person(True, death_prob, cure_prob, inf_prob, True if i < num_on_risk else False, days_before_cure))

        country = Country(healthy_pop, infect_pop)

        for day in range(days_to_check + 1):
            country.pass_day()
            infect_pops[trial][day] = country.get_infected_num()
            healthy_pops[trial][day] = country.get_healthy_num()
            dead_pops[trial][day] = country.get_dead_num()
            cure_pops[trial][day] = country.get_cure_num()

            if to_print:
                print(trial, day, infect_pops[trial][day])

            if day == start_of_quarantine:
                country.activate_quarantine(0.90)

    x_vals = range(days_to_check)
    y_vals = {}
    y_vals['Infect'] = [calc_avg_at_day(infect_pops, day) for day in x_vals]
    y_vals['Healthy'] = [calc_avg_at_day(healthy_pops, day) for day in x_vals]
    y_vals['Dead'] = [calc_avg_at_day(dead_pops, day) for day in x_vals]
    y_vals['Cure'] = [calc_avg_at_day(cure_pops, day) for day in x_vals]

    # DAY_TO_PRINT
    day_to_check = 0
    # DAY_TO_PRINT

    mean, std = calc_std(infect_pops, day_to_check)

    pylab.figure(index)
    pylab.title(
        f'{index}. The number of infected people at day 20 was of {mean} +- {1.96 * std} the 95% of the times')
    pylab.plot(x_vals, y_vals['Infect'], label='Infected')
    pylab.plot(x_vals, y_vals['Healthy'], label='Healthy')
    pylab.plot(x_vals, y_vals['Dead'], label='Dead')
    pylab.plot(x_vals, y_vals['Cure'], label='Cure')
    pylab.legend()
    pylab.xlabel('Number of the days')
    pylab.ylabel('Number of people')
    pylab.savefig(f'figures/Figure_{index}')

    data_frame = pandas.DataFrame(y_vals)
    data_frame.to_csv(f'figures/Figure_{index}.csv')


# (index, init_healthy, init_infected, death_prob, cure_prob, inf_prob, on_risk_ratio,
# days_before_cure, num_trials, days_to_check, to_print=False, start_of_quarantine=None)

sim_virus(2, 4600, 150, 0.01, 0.70, 0.31, 10, 5, 1,
          30, to_print=True, start_of_quarantine=37)


pylab.show()
