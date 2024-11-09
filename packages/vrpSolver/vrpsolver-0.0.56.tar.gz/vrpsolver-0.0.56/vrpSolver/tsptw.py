import heapq
import math
import warnings
import networkx as nx

from .common import *
from .geometry import *
from .msg import *
from .travel import *

def solveTSPTW(
    nodes: dict, 
    locFieldName: str = 'loc',
    depotID: int|str = 0,
    nodeIDs: list[int|str]|str = 'All',
    vehicles: dict = {0: {'speed': 1}},
    vehicleID: int|str = 0,
    serviceTime: float = 0,
    predefinedArcs: list[list[tuple[int|str]]] = [],
    edges: str = 'Euclidean',
    algo: str = 'IP',
    detailsFlag: bool = False,
    metaFlag: bool = False,
    **kwargs
    ) -> dict:

    # Sanity check ============================================================
    if (nodes == None or type(nodes) != dict):
        raise MissingParameterError(ERROR_MISSING_NODES)
    for i in nodes:
        if (locFieldName not in nodes[i]):
            raise MissingParameterError("ERROR: missing location information in `nodes`.")
    if (type(nodeIDs) is not list):
        if (nodeIDs == 'All'):
            nodeIDs = [i for i in nodes]
        else:
            for i in nodeIDs:
                if (i not in nodes):
                    raise OutOfRangeError("ERROR: Node %s is not in `nodes`." % i)
    if ((type(nodeIDs) == list and depotID not in nodeIDs)
        or (nodeIDs == 'All' and depotID not in nodes)):
        raise OutOfRangeError("ERROR: Cannot find `depotID` in given `nodes`/`nodeIDs`")

    if (detailsFlag == True):
        # For animation propose
        if (vehicles == None):
            raise MissingParameterError("ERROR: Missing required field `vehicles`.")
        if (vehicleID not in vehicles):
            raise MissingParameterError("ERROR: Cannot find `vehicleID` in `vehicles`.")

    if (algo == 'IP'):
        if ('solver' not in kwargs):
            kwargs['solver'] = 'Gurobi'
            kwargs['fml'] = 'MTZ'
            warnings.warn("WARNING: Missing required field `solver`, set to default 'Gurobi' with DFJ + lazy cuts")
        elif (kwargs['solver'] == 'Gurobi' and kwargs['fml'] not in ['MTZ']):
            raise OutOfRangeError("ERROR: Gurobi option s upports 'DFJ_Lazy', 'DFJ_Plainloop', 'MTZ', 'ShortestPath', 'MultiCommodityFlow', and 'QAP' formulations", )
    elif (algo == 'Heuristic'):
        if ('cons' not in kwargs and 'impv' not in kwargs):
            raise MissingParameterError(ERROR_MISSING_TSP_ALGO)

    if (predefinedArcs != None and len(predefinedArcs) > 0):
        if (not (algo == 'IP' and 'fml' in kwargs and kwargs['fml'] in ['DFJ_Lazy'])):
            raise OutOfRangeError("ERROR: TSP with pre-defined arcs is supported by DFJ_Lazy only, for now.")

    # Define tau ==============================================================
    tau = None
    path = None
    if (detailsFlag):
        tau, path = matrixDist(
            nodes = nodes, 
            nodeIDs = nodeIDs,
            edges = edges, 
            locFieldName = locFieldName,
            **kwargs)
    else:
        tau, _ = matrixDist(
            nodes = nodes, 
            nodeIDs = nodeIDs,
            edges = edges, 
            locFieldName = locFieldName,
            **kwargs)

    # Check symmetric =========================================================
    asymFlag = False
    for (i, j) in tau:
        if (tau[i, j] != tau[j, i]):
            asymFlag = True
            break

    # TSP =====================================================================
    tsp = None
    if (algo == 'IP'):
        outputFlag = None if 'outputFlag' not in kwargs else kwargs['outputFlag']
        timeLimit = None if 'timeLimit' not in kwargs else kwargs['timeLimit']
        gapTolerance = None if 'gapTolerance' not in kwargs else kwargs['gapTolerance']
        tsp = _ipTSPTWGurobiMTZ(
            nodes = nodes,
            nodeIDs = nodeIDs, 
            tau = tau, 
            outputFlag = outputFlag, 
            timeLimit = timeLimit, 
            gapTolerance = gapTolerance)
        tsp['fml'] = kwargs['fml']
        tsp['solver'] = kwargs['solver']
    else:
        raise OutOfRangeError("ERROR: Select 'algo' from ['IP'].")

    # Fix the sequence to make it start from the depot ========================
    startIndex = 0
    seq = [i for i in tsp['seq']]
    nodeSeq = []
    for k in range(len(seq)):
        if (seq[k] == depotID):
            startIndex = k
    if (startIndex <= len(seq) - 1):
        for k in range(startIndex, len(seq) - 1):
            nodeSeq.append(seq[k])
    if (startIndex >= 0):
        for k in range(0, startIndex):
            nodeSeq.append(seq[k])
    nodeSeq.append(depotID)
    tsp['seq'] = nodeSeq

    # Add service time if provided ============================================
    hasServiceTimeInfoFlag = False
    sumServiceTime = 0
    for n in nodeIDs:
        if ('serviceTime' in nodes[n]):
            sumServiceTime += nodes[n]['serviceTime']
            hasServiceTimeInfoFlag = True
    if (not hasServiceTimeInfoFlag):
        ofv = tsp['ofv'] + (len(nodeIDs) - 1) * serviceTime
    else:
        ofv = tsp['ofv'] + sumServiceTime

    # Post optimization (for detail information) ==============================
    # FIXME: Needs rewrite for TSPTW
    if (detailsFlag):
        # 返回一个数组，表示路径中的每个点的位置，不包括时间信息
        shapepoints = []        
        for i in range(len(nodeSeq) - 1):
            shapepoints.extend(path[nodeSeq[i], nodeSeq[i + 1]][:-1])
        shapepoints.append(path[nodeSeq[-2], nodeSeq[-1]][-1])

        # 返回一个数组，其中每个元素为二元数组，表示位置+时刻
        curTime = 0
        curLoc = nodes[depotID][locFieldName]
        timedSeq = [(curLoc, curTime)]
        # 对每个leg检索path中的shapepoints，涉及到serviceTime，先不看最后一段leg
        for i in range(1, len(nodeSeq) - 1):
            # 对于Euclidean型的，没有中间节点
            if (edges in ['Euclidean', 'LatLon']):
                curTime += tau[nodeSeq[i - 1], nodeSeq[i]] / vehicles[vehicleID]['speed']
                curLoc = nodes[nodeSeq[i]][locFieldName]
                timedSeq.append((curLoc, curTime))
            else:
                shapepointsInBtw = path[nodeSeq[i - 1], nodeSeq[i]]
                for j in range(1, len(shapepointsInBtw)):
                    curTime += distEuclideanXY(shapepointsInBtw[j - 1], shapepointsInBtw[j])['dist'] / vehicles[vehicleID]['speed']
                    curLoc = shapepointsInBtw[j]
                    timedSeq.append((curLoc, curTime))
            # 如果有service time，则加上一段在原处等待的时间
            if ('serviceTime' in nodes[nodeSeq[i]]):
                curTime += nodes[nodeSeq[i]]['serviceTime']
                timedSeq.append((curLoc, curTime))
            elif (serviceTime != None and serviceTime > 0):
                curTime += serviceTime
                # curLoc = curLoc
                timedSeq.append((curLoc, curTime))
        # 现在补上最后一段leg
        if (edges in ['Euclidean', 'LatLon']):
            curTime += tau[nodeSeq[-2], nodeSeq[-1]] / vehicles[vehicleID]['speed']
            curLoc = nodes[nodeSeq[-1]][locFieldName]
            timedSeq.append((curLoc, curTime))
        else:
            shapepointsInBtw = path[nodeSeq[-2], nodeSeq[-1]]
            for j in range(1, len(shapepointsInBtw)):
                curTime += distEuclideanXY(shapepointsInBtw[j - 1], shapepointsInBtw[j])['dist'] / vehicles[vehicleID]['speed']
                curLoc = shapepointsInBtw[j]
                timedSeq.append((curLoc, curTime))

        # Add detail information to `vehicles`
        vehicles[vehicleID]['shapepoints'] = shapepoints
        vehicles[vehicleID]['timedSeq'] = timedSeq

    # Add service time info ===================================================
    res = {
        'ofv': ofv,
        'seq': nodeSeq,
    }
    if (algo == 'IP'):
        res['gap'] = tsp['gap']
        res['solType'] = tsp['solType']
        res['lowerBound'] = tsp['lowerBound']
        res['upperBound'] = tsp['upperBound']
        res['runtime'] = tsp['runtime']    
    if (metaFlag):
        res['algo'] = algo
        res['serviceTime'] = serviceTime
    if (detailsFlag):
        res['vehicles'] = vehicles

    return res

def _ipTSPTWGurobiMTZ(nodes, nodeIDs, tau, outputFlag, timeLimit, gapTolerance):
    try:
        import gurobipy as grb
    except(ImportError):
        print("ERROR: Cannot find Gurobi")
        return

    # Initialize
    n = len(nodeIDs)
    TSP = grb.Model('TSP')
    if (outputFlag == False):
        TSP.setParam('OutputFlag', 0)
    if (timeLimit != None):
        TSP.setParam(grb.GRB.Param.TimeLimit, timeLimit)
    if (gapTolerance != None):
        TSP.setParam(grb.GRB.Param.MIPGap, gapTolerance)
    TSP.Params.lazyConstraints = 1

    # Decision variables ======================================================
    x = {}
    for i in range(n):
        for j in range(n):
            if i != j:
                x[i, j] = TSP.addVar(
                    vtype = grb.GRB.BINARY, 
                    obj = tau[nodeIDs[i], nodeIDs[j]], 
                    name = 'x_%s_%s' % (i, j))
    u = {}
    for i in range(n):
        u[i] = TSP.addVar(
            vtype = grb.GRB.CONTINUOUS,
            name = 'u_%s' % (i))

    # TSP objective function ==================================================
    TSP.modelSense = grb.GRB.MINIMIZE
    TSP.update()

    # Degree constraints ======================================================
    for i in range(n):
        TSP.addConstr(grb.quicksum(x[i, j] for j in range(n) if i != j) == 1, name = 'leave_%s' % str(i))
        TSP.addConstr(grb.quicksum(x[j, i] for j in range(n) if i != j) == 1, name = 'enter_%s' % str(i))

    # Sequence constraints ====================================================
    for i in range(1, n):
        for j in range(1, n):
            if (i != j):
                TSP.addConstr(u[i] - u[j] + (n - 1) * x[i, j] <= n - 2, name = 'seq_%s_%s' % (i, j))
    for i in range(1, n):
        TSP.addConstr(1 <= u[i])
        TSP.addConstr(u[i] <= n - 1)

    # Time windows ============================================================
    TSP._u = u
    def checkTW(model, where):
        if (where == grb.GRB.Callback.MIPSOL):
            u_sol = model.cbGetSolution(model._u)
            for i in range(n):
                if (nodes[nodeIDs[i]]['te'] < u_sol[i]
                    or nodes[nodeIDs[i]]['ts'] > u_sol[i]):
                    model.cbLazy(u[i] >= nodes[nodeIDs[i]]['ts'])
                    model.cbLazy(u[i] <= nodes[nodeIDs[i]]['te'])

    # TSP =====================================================================
    TSP.optimize(checkTW)

    # Reconstruct solution ====================================================
    ofv = None
    gap = None
    seq = []
    arcs = []
    solType = None
    lb = None
    ub = None
    runtime = None

    ofv = TSP.getObjective().getValue()
    gap = TSP.Params.MIPGapAbs
    for i, j in x:
        if (x[i, j].x > 0.5):
            arcs.append([i, j])
    currentNode = 0
    seq.append(nodeIDs[currentNode])
    while (len(arcs) > 0):
        for i in range(len(arcs)):
            if (arcs[i][0] == currentNode):
                currentNode = arcs[i][1]
                seq.append(nodeIDs[currentNode])
                arcs.pop(i)
                break    
    if (TSP.status == grb.GRB.status.OPTIMAL):
        solType = 'IP_Optimal'
        gap = 0
        lb = ofv
        ub = ofv
        runtime = TSP.Runtime
    elif (TSP.status == grb.GRB.status.TIME_LIMIT):
        solType = 'IP_TimeLimit'
        gap = TSP.MIPGap
        lb = TSP.ObjBoundC
        ub = TSP.ObjVal
        runtime = TSP.Runtime

    return {
        'ofv': ofv,
        'seq': seq,
        'gap': gap,
        'solType': solType,
        'lowerBound': lb,
        'upperBound': ub,
        'runtime': runtime
    }
