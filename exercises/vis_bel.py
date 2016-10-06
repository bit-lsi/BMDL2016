from IPython.display import IFrame
import json

def vis_network(nodes, edges):
    html = """
        <!doctype html>
        <html><head>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis.min.js"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis.min.css" rel="stylesheet" type="text/css" />
        <style type="text/css">
        #mynetwork {width: 950px;height: 750px;border: 1px solid lightgray;}
        </style>
        </head>
        <body>
        <div id="mynetwork"></div>
        <script type="text/javascript">
        var visjs_data = {};
        visjs_data.nodes = %s;
        visjs_data.edges = %s;
        </script>
        <script type="text/javascript">
// color for vis.js networks
var relColor = {
	'decreases' : "red",
	'directlyDecreases' : "red",
	'increases' : "green",
	'directlyIncreases' : "green",
	'causesNoChange' : "#088A08",
	'negativeCorrelation' : "#610B0B",
	'positiveCorrelation' : "#5F4C0B",
	'association' : "#190710",
	'analogous' : "#DF01D7",
	'orthologous' : "#243B0B",
	'transcribedTo' : "#58FAF4",
	'translatedTo' : "#2EFE2E",
	'biomarkerFor' : "#2EFE2E",
	'hasMember' : "#2EFE2E",
	'hasMembers' : "#2EFE2E",
	'hasComponent' : "#2EFE2E",
	'hasComponents' : "#2EFE2E",
	'isA' : "#2EFE2E",
	'prognosticBiomarkerFor' : "#2EFE2E",
	'rateLimitingStepOf' : "#2EFE2E",
	'subProcessOf' : "#2EFE2E"
};

var borderColor = {
		'gtp' : "#FF0000",
		'tloc' : "#DBA901",
		'tscript' : "#04B404",
		'act' : "#0101DF",
		'sec' : "#B404AE",
		'phos' : "#DF013A",
		'surf' :  "#585858",
		'tport' : "#01DFA5",
		'deg' : "#F7819F",
		'ribo' : "#D0FA58",
		'kin' : "#9F81F7",
		'cat' : "purple",
		'chap' : "#8A0886",
		'pep' : "#084B8A"
}; 
var nodesColor = {
		'p' : "red",
		'a' : "purple",
		'g' : "green",
		'path' : "orange",
		'complex' : "blue",
		'bp' : "cyan",
		'rxn' :  "lime green",
		'list' : "green",
		'composite' : "Fuchsia",
		'r' : "Teal",
		'm' : "Gold",
		null : "Gold",
}; 
var nodesShape = {
		'p' : "diamond",
		'a' : "star",
		'g' : "triangle",
		'path' : "triangleDown",
		'complex' : "square",
		'bp' : "dot",
		'rxn' :  "square",
		'list' : "star",
		'composite' : "diamond",
		'r' : "dot",
		'reaction' : "dot",
		'm' : "dot",
		null : "dot",
};
        
        </script>
        <script type="text/javascript">
function startNetwork(d) {
console.log(d.nodes);
console.log(d.edges);
	// add color feature to edges
	for (i = 0; i < d.edges.length; i++) {
		d.edges[i]["color"] = relColor[d.edges[i].label];
	}
	;
	// add color feature to nodes
	for (i = 0; i < d.nodes.length; i++) {
		if (d.nodes[i].act != null){ 
			d.nodes[i]["borderWidth"] = 3;
			d.nodes[i]["color"] = {background:(nodesColor[d.nodes[i].group]),border:(borderColor[d.nodes[i].act])};
		}
		else{
			d.nodes[i]["color"] = nodesColor[d.nodes[i].group];
		}
	}
	;
	// add shape feature to nodes
	for (i=0; i<d.nodes.length; i++){
		d.nodes[i]["shape"] = nodesShape[d.nodes[i].group];
	}
	;
	var nodesDict={};
        for (i = 0; i < d.nodes.length; i++) {
            nodesDict[d.nodes[i].id] = d.nodes[i].label;
        }
        ;

	var nodes = new vis.DataSet(d.nodes);
	
	// create an array with edges
	var edges = new vis.DataSet(d.edges);

	// create a network
	var container = document.getElementById('mynetwork');
	var data = {
		nodes : nodes,
		edges : edges
	};
	var options = {
		interaction : {
			hideEdgesOnDrag : true
		},
		edges : {
			arrows : 'to',
			label : 'middle',
			font : {
				align : 'middle'
			},
			smooth : {
				type : 'continuous'
			}
		},
		physics : {
			"minVelocity": 0.25,
			barnesHut : {
				gravitationalConstant : -10000,
				springConstant : 0.01,
				springLength : 150,
				avoidOverlap : 0.1
			
			}
		}
	};
	var network = new vis.Network(container, data, options);
};
startNetwork(visjs_data);
        </script>
        </body>
        </html>
    """ % (json.dumps(nodes),json.dumps(edges))

    filename = "graph-temp.html"

    file = open(filename, "w")
    file.write(html)
    file.close()

    return IFrame(filename, width="1000", height="800")

def draw(g):
    nodes = g.nodes(data=True)
    node_list = []
    edge_list = []
    
    for node_id, node_attribs in nodes:
        node_dict = {'id':node_id}
        if 'BEL' in node_attribs:
            node_dict['label'] = node_attribs['BEL']
            node_dict['group'] = node_attribs['function']
        node_list.append(node_dict)
    
    # node[0] = node_id
    nodeId_index_dict = {node[0]:index for index,node in enumerate(nodes)}
        
    for source, target, edge_attribs in g.edges(data=True):
        #edge_dict = {'from':nodeId_index_dict[source], 'to':nodeId_index_dict[target]} 
        edge_dict = {'from':source, 'to':target} 
        if 'rel' in edge_attribs:
            edge_dict['label'] = edge_attribs['rel']
        edge_list.append(edge_dict)    

    #return node_list,edge_list
    return vis_network(node_list,edge_list)

