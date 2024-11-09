from typing import List, Set

from box import Box

type NodeId = str
type TaskId = str


class TaskNodeInfo(object):
    node_id: NodeId
    node_name: str = None

    def __str__(self):
        return f'node_id={self.node_id},node_name={self.node_name}'

    def __eq__(self, other):
        if isinstance(other, TaskNodeInfo):
            return other.node_id == self.node_id
        return False

    def __hash__(self):
        return hash(self.node_id)


def add_node_pair_1(from_node: TaskNodeInfo, to_node: TaskNodeInfo,
                    d: dict[NodeId, List[TaskNodeInfo]]) -> None:
    """
    辅助类
    @param from_node:
    @param to_node:
    @param d:
    @return:
    """
    if from_node is None:
        return
    from_node_id: NodeId = from_node.node_id
    if from_node_id in d:
        if to_node is not None and to_node.node_id not in [it.node_id for it in d[from_node_id]]:
            d[from_node_id].append(to_node)
        else:
            return
    else:
        d[from_node_id] = []
        if to_node is not None:
            d[from_node_id] = list([to_node])


class TaskNodeGraph(object):
    child_node_map: dict[NodeId, List[TaskNodeInfo]] = {}
    parent_node_map: dict[NodeId, List[TaskNodeInfo]] = {}
    all_node_id_set: Set[TaskNodeInfo] = set()
    # 任务节点的深度树,key是深度从0,开始
    task_node_tree: dict[int, List[TaskNodeInfo]] = {}

    def __init__(self):
        pass

    def get_startup_nodes(self) -> List[TaskNodeInfo]:
        """获取执行启动节点"""
        # 没有父节点的便是启动节点
        nodes: List[TaskNodeInfo] = []
        for it in self.all_node_id_set:
            if it.node_id not in self.parent_node_map:
                nodes.append(it)
                continue
            parent_nodes: List[TaskNodeInfo] = self.parent_node_map[it.node_id]
            if parent_nodes is None or len(parent_nodes) == 0:
                nodes.append(it)
        return nodes

    def __build_node_tree(self, in_tree_nodes: Set[NodeId], tree_depth: int) -> None:
        """
        递归获取深度,思路：遍历所有节点判断每个节点的所有父节点是否都已经在depth<= tree_depth的树上，如果是，那么就绑定到当前深度上
        其他继续遍历,直至所有节点都被访问过
        @param in_tree_nodes:
        @param tree_depth:
        @return:
        """
        if in_tree_nodes is None or len(in_tree_nodes) == 0:
            return
        # 如果入列的所有元素数量和图一致，代表遍历完了
        if len(in_tree_nodes) == len(self.all_node_id_set):
            return
        if tree_depth not in self.task_node_tree:
            self.task_node_tree[tree_depth] = []
        for i in self.all_node_id_set:
            curr_node_id: NodeId = i.node_id
            if curr_node_id in in_tree_nodes:
                continue
            curr_parent_nodes: List[TaskNodeInfo] = self.parent_node_map.get(curr_node_id, [])
            match_curr_depth: bool = True
            for j in curr_parent_nodes:
                if j.node_id not in in_tree_nodes:
                    match_curr_depth = False
                    break
            if match_curr_depth:
                self.task_node_tree[tree_depth].append(i)
        # 获取所有小于此深度的所有元素
        in_tree_nodes1: List[NodeId] = list(in_tree_nodes) + [k.node_id for k in
                                                              self.task_node_tree.get(tree_depth, [])]
        tree_depth = tree_depth + 1
        self.__build_node_tree(set(in_tree_nodes1), tree_depth)

    def build_node_tree(self) -> None:
        """
        刷新树结构,必须要节点添加完毕,到时候可以研究下一定要调用这个方法才能访问属性
        @return:
        """
        # 获取根节点
        startup_nodes: List[TaskNodeInfo] = self.get_startup_nodes()
        if startup_nodes is None or len(startup_nodes) == 0:
            return
        self.task_node_tree[0] = startup_nodes
        self.__build_node_tree(set([k.node_id for k in startup_nodes]), 1)

    def add_node_pair(self, from_node: TaskNodeInfo | None, to_node: TaskNodeInfo | None) -> None:
        """
        register node pair
        @param from_node:
        @param to_node:
        @return:
        """
        # logger.info(f"from_node={from_node} ----> to_node={to_node}")
        add_node_pair_1(from_node, to_node, self.child_node_map)
        add_node_pair_1(to_node, from_node, self.parent_node_map)
        # 添加所有出现过的节点
        if from_node is not None:
            self.all_node_id_set.add(from_node)
        if to_node is not None:
            self.all_node_id_set.add(to_node)

    def get_child_nodes(self, parent_node_id: NodeId) -> List[TaskNodeInfo]:
        """
        获取子节点列表
        @param parent_node_id:
        @return:
        """
        return self.child_node_map.get(parent_node_id, [])

    def get_parent_nodes(self, child_node_id: NodeId) -> List[TaskNodeInfo]:
        """
        获取父节点列表
        @param child_node_id:
        @return:
        """
        return self.parent_node_map.get(child_node_id, [])


class TaskInfo(object):
    task_id: None
    task_name: str = None
    task_exec_type: str = None
    sched_info: any
    node_graph: TaskNodeGraph = TaskNodeGraph()
    task_config: Box
