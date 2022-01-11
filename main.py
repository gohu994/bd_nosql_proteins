import graph
import similarites
from neo4j import GraphDatabase


def main():
    #similarites.compute_matrix('datas/matrix_tri_test.csv')
    # graph.graph_creation()
    #
    graph.delete()
    graph.create()
if __name__ == "__main__":
    main()
