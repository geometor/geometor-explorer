"""
test script for geometor package
"""
from geometor import *

if __name__ == '__main__':

    sp.init_printing()

    NAME = 'vesica'
    NAME += input(f'\nsession name: {NAME}')
    log_init(NAME)
    start_time = timer()

    print_log(f'\nMODEL: {NAME}')

    M = Model()
    # TODO: add label to Models
    A = M.gen_point(0, 0)
    B = M.gen_point(1, 0)
    l1 = M.gen_line(A, B)
    c1 = M.gen_circle(A, B)
    c2 = M.gen_circle(B, A)
    print(M)
    M.summary()

    # PLOT *********************************
    print_log(f'\nPLOT: {NAME}')

    fig, (ax, ax_btm) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [10, 1]})
    plt.tight_layout()

    plot_model(NAME, ax, ax_btm, M)

    #  title = f'G E O M E T O R'
    #  fig.suptitle(title, fontdict={'color': '#960', 'size':'small'})


    #  print_log('\nPlot Build')
    #  build_sequence(NAME, ax, ax_btm, m, bounds)

    #  bounds = get_bounds_from_sections(goldens)

    #  print_log('\nPlot Goldens')
    #  plot_sections(NAME, ax, ax_btm, history, goldens, bounds)

    #  print_log('\nPlot Golden Groups')
    #  plot_all_groups(NAME, ax, ax_btm, history, groups, bounds)

    #  plot_all_sections(NAME, ax, ax_btm, history, goldens, bounds)

    #  complete_summary(NAME, start_time, goldens, groups)

    plt.show()
