FIG_W = 16
FIG_H = 9

def snapshot(folder, filename):
    import os
    sessions = os.path.expanduser('~') + '/Sessions'
    out = f'{sessions}/{folder}/'
    os.makedirs(out, exist_ok=True)
    plt.savefig(out + filename, dpi=120)
    print_log(f'    * {out + filename}')


def display(filename):
    from IPython import display
    display.Image(filename)



def ax_prep(ax, ax_btm, bounds, xlabel):
    ax.clear()
    ax_btm.clear()
    ax.axis(False)
    ax_btm.axis(False)
    #  ax.spines['bottom'].set_color('k')
    #  ax.spines['top'].set_color('k')
    #  ax.spines['right'].set_color('k')
    #  ax.spines['left'].set_color('k')
    #  ax.tick_params(axis='x', colors='k')
    #  ax.tick_params(axis='y', colors='k')
    vmin = bounds.vertices[0]
    vmax = bounds.vertices[2]
    ax.set_xlim(float(vmin.x.evalf()), float(vmax.x.evalf()))
    ax.set_ylim(float(vmin.y.evalf()), float(vmax.y.evalf()))
    ax.invert_yaxis()

    #  ax.set_xlabel(xlabel, fontdict={'color': 'w', 'size':'20'})
    ax_btm.text(0.5, 0.5, xlabel, ha='center', va='center', fontdict={'color': 'w', 'size':'20'})


def get_limits_from_points(pts, margin=1):
    '''find x, y limits from a set of points'''
    limx = [0, 0]
    limy = [0, 0]
    if pts:
        pt = list(pts)[0]
        ptx = float(pt.x.evalf())
        pty = float(pt.y.evalf())
        limx[0] = ptx
        limx[1] = ptx
        limy[0] = pty
        limy[1] = pty

        for pt in pts:
            ptx = float(pt.x.evalf())
            pty = float(pt.y.evalf())
            # print(x, y)
            limx[0] = ptx if ptx < limx[0] else limx[0]
            limx[1] = ptx if ptx > limx[1] else limx[1]
            limy[0] = pty if pty < limy[0] else limy[0]
            limy[1] = pty if pty > limy[1] else limy[1]

    limx[0] -= margin
    limx[1] += margin
    limy[0] -= margin
    limy[1] += margin

    return [limx, limy]


def get_bounds_from_sections(sections, r=FIG_W/(FIG_H-1)):
    section_pts = set()
    for i, section in enumerate(sections):
        for seg in section:
            for pt in seg.points:
                section_pts.add(pt)
    limx, limy = get_limits_from_points(section_pts, margin=.25)
    limx, limy = adjust_lims(limx, limy, r=r)
    bounds = set_bounds(limx, limy)
    return bounds


