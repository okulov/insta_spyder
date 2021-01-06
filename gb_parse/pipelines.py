# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pickle, sys


class GbParsePipeline:

    def process_item(self, item, spider):
        with open(spider.file, 'rb') as f:
            graph_f = pickle.load(f)
        graph_f['data'][item['side']][item['id']] = item['graph']
        graph_f['data'][item['side']]['all'].update(item['graph'])
        other_side = str(2 // int(item['side']))
        if item['id'] in graph_f['data'][other_side]['all']:  # если есть сходимость частей
            graph_f['chance_to_way'] = True
            graph_f['data']['1'].update(graph_f['data']['2'])  # объединяем части
            all_graph = graph_f['data']['1']
            graph_f['way_list'] = self.bfs(all_graph, graph_f['target_user'][0], graph_f['target_user'][1])
            print(f'Путь возможен и найден: {graph_f["way_list"]}')
            with open(spider.file, 'wb') as f:
                pickle.dump(graph_f, f)
            sys.exit()
        with open(spider.file, 'wb') as f:
            pickle.dump(graph_f, f)
        print(item['id'])
        return item

    # поиск пути по графу
    def bfs(self, graph, start, finish):
        D = [None] * (len(graph) + 1)
        Prev = [None] * (len(graph) + 1)
        D[start] = 0
        Q = [start]
        Qstart = 0
        while Qstart < len(Q):
            u = Q[Qstart]
            Qstart += 1
            for v in graph[u]:
                if D[v] is None:
                    Prev[v] = u
                    D[v] = D[u] + 1
                    Q.append(v)
        Ans = []
        curr = finish
        while curr is not None:
            Ans.append(curr)
            curr = Prev[curr]
        return Ans
