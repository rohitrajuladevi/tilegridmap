def tilegrid(shapeoutline, shapeborders, namena, interpolation=1, xshift=0, yshift=0, starting=False):
    import geopandas as gpd
    import matplotlib.pyplot as plt
    from shapely.geometry import Point
    from shapely.geometry.polygon import Polygon
    import pandas as pd
    import math as m
    import numpy as np
    from shapely.geometry import Point
    from shapely.geometry.polygon import Polygon
    from scipy.optimize import linear_sum_assignment
    fp = shapeborders
    gdf = gpd.read_file(fp)
    gdf = gdf.to_crs(3857)

    gdf['NAME'] = gdf[namena]

    gdf2 = gpd.read_file(shapeoutline)
    gdf2 = gdf2.to_crs(3857)



    mycoordslist = [list(x.exterior.coords) for x in gdf2.iloc[0].geometry.geoms]
    mycoordslist.sort(key=len)
    mycoordslist.reverse()

    gdf['Centroids'] = gdf['geometry'].centroid
    maxlist=mycoordslist[0]
    maxlist=np.asarray(maxlist)

    bpolygon = Polygon(maxlist)
    droplist=[]
    for i in range(len(gdf)):
        if(bpolygon.contains(gdf.iloc[i].Centroids)==False):
            droplist.append(i)
    droplist.reverse()
    if(len(droplist)!=0):
        for i in range(len(droplist)):
            gdf.drop(droplist[i], inplace = True)

    import numpy as np

    def borders(gdf):

        # add NEIGHBORS column
        gdf["NEIGHBORS"] = None  

        for index, country in gdf.iterrows():   

            # get 'not disjoint' countries
            neighbors = gdf[~gdf.geometry.disjoint(country.geometry)].NAME.tolist()

            # remove own name of the country from the list
            neighbors = [ name for name in neighbors if country.NAME != name ]

            # add names of neighbors as NEIGHBORS value
            gdf.at[index, "NEIGHBORS"] =neighbors

    def xyplot(gdf):
        gdf = gdf.reset_index()
        emptLst1 = []
        emptLst2 = []
        for k in range(len(gdf)):
            emptLst1.append([])
            emptLst2.append([])

        gdf['X'] = emptLst1.copy()
        gdf['Y'] = emptLst2.copy()

        for j in range(len(gdf)):
            for i in gdf.iloc[j]['NEIGHBORS']:
                gdf.iloc[j]["X"].append([gdf.iloc[j]["Centroids"].x, gdf.iloc[gdf.index[gdf['NAME']==i].tolist()[0]]['Centroids'].x])
                gdf.iloc[j]["Y"].append([gdf.iloc[j]["Centroids"].y, gdf.iloc[gdf.index[gdf['NAME']==i].tolist()[0]]['Centroids'].y])
        return gdf


    borders(gdf)
    gdf=xyplot(gdf)
    
    droplist=[]
    for i in range(len(gdf)):
        if(len(gdf.iloc[i].NEIGHBORS)==0):
            droplist.append(i)
    droplist.reverse()
    if(len(droplist)!=0):
        for i in range(len(droplist)):
            gdf.drop(droplist[i], inplace = True)




    xcentr=[]
    ycentr=[]
    for i in range(len(gdf['Centroids'])):
        xcentr.append(gdf['Centroids'][i].x)
        ycentr.append(gdf['Centroids'][i].y)
    xcentr = np.asarray(xcentr)
    ycentr = np.asarray(ycentr)


    import math as m

    stepsize = m.sqrt(gdf['geometry'].area.sum()/len(gdf['geometry']))



    def xyplot2(gdf):
        emptLst1 = []
        emptLst2 = []
        for k in range(len(gdf)):
            emptLst1.append([])
            emptLst2.append([])

        gdf['X'] = emptLst1.copy()
        gdf['Y'] = emptLst2.copy()

        for j in range(len(gdf)):
            for i in gdf.iloc[j]['NEIGHBORS']:
                gdf.iloc[j]["X"].append([gdf.iloc[j]["Updated Centroids"][0], gdf.iloc[gdf.index[gdf['NAME']==i].tolist()[0]]['Updated Centroids'][0]])
                gdf.iloc[j]["Y"].append([gdf.iloc[j]["Updated Centroids"][1], gdf.iloc[gdf.index[gdf['NAME']==i].tolist()[0]]['Updated Centroids'][1]])
        return gdf

    for i in range(30):
        npcentr=[]
        gdf['Updated Centroids']=None
        for i in range(len(gdf)):
            sum = np.asarray([0,0])
            card = len(gdf.iloc[i]['X'])
            for j in range(card):
                po =np.asarray([gdf.iloc[i]['X'][j][0], gdf.iloc[i]['Y'][j][0]])
                bpo=np.asarray([gdf.iloc[i]['X'][j][1], gdf.iloc[i]['Y'][j][1]])
                sum= sum+(bpo+stepsize*(po-bpo)/np.linalg.norm(po-bpo))
            sum=sum/card
            for j in range(card):
                gdf.iloc[i]['X'][j][0]=sum[0]
                gdf.iloc[i]['Y'][j][0]=sum[1]
            npcentr.append(sum)
            gdf['Updated Centroids'][i] = sum
        gdf=xyplot2(gdf)


    npcentr=np.asarray(npcentr)


    mycoordslist = [list(x.exterior.coords) for x in gdf2.iloc[0].geometry.geoms]
    max=0
    for i in range(len(mycoordslist)):
        if(len(mycoordslist[i])>max):
            max=len(mycoordslist[i])
            maxlist=mycoordslist[i]
    maxlist=np.asarray(maxlist)

    intlst=[]
    for i in range(len(maxlist)):
        intlst.append(i)
    intlst=np.asarray(intlst)
    try:
        x= np.random.choice(intlst,1000, replace=False)
        x.sort()
        y=[]
        for i in range(len(x)):
            y.append(maxlist[x[i]])
        maxlist=np.asarray(y)
    except:
        pass


    emptLst = []
    for k in range(len(gdf)):
        emptLst.append([0,0])

    centroidsfre=[]
    for i in range(len(gdf)):
        centroidsfre.append([gdf.iloc[i]['Centroids'].x, gdf.iloc[i]['Centroids'].y])

    centroidsfre = np.asarray(centroidsfre)

    gdf['Starting Centroids'] = emptLst

    for i in range (len(centroidsfre)):
        gdf['Starting Centroids'][i]=centroidsfre[i]




    for i in range(len(gdf)):
        gdf['Updated Centroids'][i]= (centroidsfre+interpolation*(centroidsfre-npcentr))[i]
        npcentr[i]=(centroidsfre+interpolation*(centroidsfre-npcentr))[i]



    def nearestcent(maxlist,gdf):
        closestlist=[]


        for j in range(len(maxlist)):
            fir=np.linalg.norm(gdf.iloc[0]["Starting Centroids"]-maxlist[0])*100
            sec=np.linalg.norm(gdf.iloc[0]["Starting Centroids"]-maxlist[0])*100
            thir=np.linalg.norm(gdf.iloc[0]["Starting Centroids"]-maxlist[0])*100
            thirn=[]
            secn=[]
            firn=[]

            for i in range(len(gdf)):
                dist = np.linalg.norm(gdf.iloc[i]["Starting Centroids"]-maxlist[j])

                if(dist<thir and not(dist<sec)):
                    thir = dist
                    thirn = [gdf.iloc[i]["Starting Centroids"],gdf.iloc[i]["Updated Centroids"]]

                if(dist<sec and not(dist<fir)):
                    thir = sec
                    thirn = secn

                    sec=dist
                    secn = [gdf.iloc[i]["Starting Centroids"],gdf.iloc[i]["Updated Centroids"]]

                if(dist<fir):
                    thir = sec
                    thirn = secn

                    sec = fir
                    secn = firn

                    fir=dist
                    firn = [gdf.iloc[i]["Starting Centroids"],gdf.iloc[i]["Updated Centroids"]]

            closestlist.append([firn,secn,thirn])


        return closestlist


    closestlist = np.asarray(nearestcent(maxlist,gdf))

    weights=[]
    vik=[]
    for i in range(len(maxlist)):
        indw=[]
        vikw=[]
        for j in range(len(closestlist[i])):
            wei=-1*(np.linalg.norm(maxlist[i]-closestlist[i][j][0])**2)/(2*np.linalg.norm(maxlist[i]-closestlist[i][0][0])**2)
            wei=m.exp(wei)
            indw.append(wei)
            vikw.append((maxlist[i]-closestlist[i][j][0])*wei)

        indw=np.asarray(indw)
        indw=indw/indw.sum()

        sum=np.asarray([0,0])
        for j in range(len(indw)):
            sum=sum+(maxlist[i]-closestlist[i][j][0])*indw[j]

        weights.append(indw)
        vik.append(sum)
    weights=np.asarray(weights)
    vik=np.asarray(vik)

    smplist=[]
    for i in range(len(closestlist)):
        sum=np.asarray([0,0])
        for j in range(len(weights[i])):
            sum=sum+closestlist[i][j][1]*weights[i][j]
        smplist.append(sum)

    smplist=np.asarray(smplist)
    magvik=[]
    for i in range(len(vik)):
        magvik.append(np.linalg.norm(vik[i]))

    magvik=np.asarray(magvik)

    updatedvik=[]
    for i in range(len(vik)):
        updatedvik.append(np.sqrt(stepsize/magvik[i])*vik[i])
    updatedvik = np.asarray(updatedvik)

    newboundary=smplist+updatedvik

    from shapely.geometry import Point
    from shapely.geometry.polygon import Polygon

    point = Point(-90, 30)
    polygon = Polygon(newboundary)

    origin = np.amin(newboundary, axis=0)
    maxpo=np.amax(newboundary, axis=0)

    def grid(origin, maxpo, stepsize, polygon, npcentr, xshift=0, yshift=0):
        inside=[]

        while(len(inside)!=len(npcentr)):
            if(len(inside)>len(npcentr) and len(inside)!=0):
                stepsize = stepsize + stepsize/50
            if(len(inside)<len(npcentr) and len(inside)!=0):
                stepsize = stepsize - stepsize/50

            minx= origin[0]-stepsize*xshift
            maxx= maxpo[0]
            miny= origin[1]-stepsize*yshift
            maxy= maxpo[1]

            xarr=[]
            yarr=[]
            gridsize=[]
            position=[]
            inside=[]

            while(minx<=maxx):
                xarr.append(minx)
                minx+=stepsize
            while(miny<=maxy):
                yarr.append(miny)
                miny+=stepsize

            gridsize.append(len(xarr))
            gridsize.append(len(yarr))


            for i in range(len(xarr)):
                for j in range(len(yarr)):  
                        if(polygon.contains(Point(xarr[i],yarr[j]))):
                            inside.append([xarr[i],yarr[j]])
                            position.append([i,gridsize[1]-j])
        return [inside,position,gridsize]

    tiles, position, gridsize =grid(origin,maxpo,stepsize,polygon,npcentr, xshift, yshift)

    position=np.asarray(position)
    np.amin(position, axis=0)
    position = position - np.amin(position, axis=0)

    gridsize=np.amax(position, axis=0)+1

    position=position.tolist()
    gridsize=gridsize.tolist()

    tiles=np.asarray(tiles)

    A=[]
    for i in range(len(gdf)):
        A.append([])
        for j in range(len(tiles)):
            if(starting==True):
                A[i].append(np.linalg.norm(gdf.iloc[i]['Starting Centroids']-tiles[j])**2)
            else:
                A[i].append(np.linalg.norm(gdf.iloc[i]['Updated Centroids']-tiles[j])**2)
    A= np.asarray(A)

    from scipy.optimize import linear_sum_assignment
    row_ind, col_ind = linear_sum_assignment(A)

    matching=[]
    for i in range(col_ind.max()+1):
        matching.append('')
    for i in range(len(col_ind)):
        matching[col_ind[i]]= gdf.iloc[i].NAME

    position = np.asarray(position)
    np.amin(position, axis=0)
    position = position - np.amin(position, axis=0)

    gridsize = np.amax(position, axis=0) + 1

    position = position.tolist()
    gridsize = gridsize.tolist()

    tiles = np.asarray(tiles)

    A = []
    for i in range(len(gdf)):
        A.append([])
        for j in range(len(tiles)):
            if (starting == True):
                A[i].append(np.linalg.norm(gdf.iloc[i]['Starting Centroids'] - tiles[j]) ** 2)
            else:
                A[i].append(np.linalg.norm(gdf.iloc[i]['Updated Centroids'] - tiles[j]) ** 2)
    A = np.asarray(A)

    row_ind, col_ind = linear_sum_assignment(A)

    matching = []
    for i in range(col_ind.max() + 1):
        matching.append('')
    for i in range(len(col_ind)):
        matching[col_ind[i]] = gdf.iloc[i].NAME

    newmatching = []
    newposition = []

    count = 0

    for i in range(gridsize[0]):
        for j in range(gridsize[1] - 1, -1, -1):
            if ([i, j] in position):
                newmatching.append(matching[count])
                newposition.append([i, j])
                count = count + 1

    newtiles = []
    for i in range(len(tiles)):
        newtiles.append(tiles[i])
    df1 = pd.DataFrame()
    df1['NAMES'] = newmatching
    df1['Position'] = newposition
    df1['Tile Coordinates'] = newtiles
    df1['Grid Size'] = str(gridsize)
    plah = []
    for i in range(len(df1)):
        plah.append(gridsize)
    df1['Grid Size'] = plah
    plah = []
    for i in range(len(df1)):
        plah.append(stepsize)
    df1['Stepsize'] = plah
    df1.to_excel("tilegrid.xlsx")