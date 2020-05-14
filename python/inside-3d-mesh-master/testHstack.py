
filenames = np.asarray([
  np.hstack(filenames[IsPointInside[i].flatten()]) for i in range(0, len(Grid))]).flatten()
