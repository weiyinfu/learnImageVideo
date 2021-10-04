from skimage import data, viewer

viewer.CollectionViewer([
    data.moon(),
    data.text(),
    data.astronaut(),
    data.camera(),
    data.checkerboard(),
    data.chelsea(),
    data.clock(),
    data.coffee(),
    data.coins(),
    data.rocket(),
    data.page(),
    data.immunohistochemistry()
]).show()
viewer.ImageViewer(data.chelsea()).show()
