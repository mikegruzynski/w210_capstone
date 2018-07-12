class RadarPlot(object):
    def __init__(self):
        pass

    class RadarAxes():

        def __init__(self, *args, **kwargs):
            super(RadarAxes, self).__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

            self.name = 'radar'
            # use 1 line segment to connect specified points
            self.RESOLUTION = 1
            # define draw_frame method
            self.draw_patch = patch_dict[frame]

