import os
import arcpy


def diffValue(in_raster1, in_raster2, in_raster3, value):
    inRaster1 = arcpy.RasterToNumPyArray(in_raster1)
    inRaster2 = arcpy.RasterToNumPyArray(in_raster2)
    inRaster3 = arcpy.RasterToNumPyArray(in_raster3)
    TP, TN, FP, FN = 0, 0, 0, 0

    rows = inRaster1.shape[0]
    cols = inRaster1.shape[1]
    print rows, cols
    for i in xrange(0, rows):
        for j in xrange(0, cols):
            if not inRaster1[i, j]:
                continue

            if inRaster1[i, j] != value:
                if inRaster2[i, j] != value:
                    if inRaster3[i, j] != value:
                        TN += 1
                    else:
                        FP += 1
                else:
                    if inRaster3[i, j] != value:
                        FN += 1
                    else:
                        TP += 1
            else:
                if inRaster2[i, j] != value:
                    if inRaster3[i, j] != value:
                        TP += 1
                    else:
                        FN += 1
                else:
                    if inRaster3[i, j] != value:
                        FP += 1
                    else:
                        TN += 1

    PCM_P = TP / float(TP + FN) if (TP + FN) > 0 else 0
    PCM_N = TN / float(TN + FP) if (TN + FP) > 0 else 0
    return (PCM_P, PCM_N)


def diff(in_raster1, in_raster2, in_raster3, in_values, out_csv):
    ext = os.path.splitext(out_csv)[1]
    if ext != '.csv':
        out_csv += '.csv'
    f = open(out_csv, 'w')
    f.write('Value, PCM_P, PCM_N\n')

    for value in in_values:
        PCM_P, PCM_N = diffValue(in_raster1, in_raster2, in_raster3, int(value))
        f.write('{0}, {1}, {2}\n'.format(value, PCM_P, PCM_N))

    f.close()


if __name__ == "__main__":
    in_raster1 = arcpy.GetParameterAsText(0)
    in_raster2 = arcpy.GetParameterAsText(1)
    in_raster3 = arcpy.GetParameterAsText(2)
    in_values = arcpy.GetParameterAsText(3).split(";")
    out_csv = arcpy.GetParameterAsText(4)

    diff(in_raster1, in_raster2, in_raster3, in_values, out_csv)
