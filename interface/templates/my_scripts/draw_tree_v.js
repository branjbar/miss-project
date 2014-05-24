
var margin = {top: 40, right: 20, bottom: 50, left: 20},
    width = 550 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

var tree = d3.layout.tree()
    .separation(function(a, b) { return a.parent === b.parent ? 1 : 1.2; })
    .children(function(d) { return d.parents; })
    .size([width, height]);

var svg = d3.select("#graph1")
    .attr("bgcolor", "#2c2c2c")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
   .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        json = JSON.parse( '{{json_dict|tojson|safe}}' )
          var nodes = tree.nodes(json);

var node = svg.selectAll(".node")
    .data(nodes)
   .enter()
    .append("g");

node.append("rect")
    .attr("width", width/4.5)
    .attr("height", 80)
    .attr("fill", "Linen ")
    .attr("x", function(d) { return d.x - width/9; })
    .attr("y", function(d) { return height - d.y - 40; });

node.append("text")
     .attr("class", "name")
    .attr("x", function(d) { return d.x; })
    .attr("y", function(d) { return height - d.y - 25; })
    .style("text-anchor", "middle")
    .text(function(d) { return d.fname; });

node.append("text")
     .attr("class", "name")
    .attr("x", function(d) { return d.x; })
    .attr("y", function(d) { return height - d.y - 15; })
    .style("text-anchor", "middle")
    .text(function(d) { return d.lname; });

node.append("text")
     .attr("class", "id")
    .attr("x", function(d) { return d.x; })
    .attr("y", function(d) { return height - d.y ; })
    .style("text-anchor", "middle")
    .text(function(d) { return d.id ? '(' + d.id + ')' : ''; });

node.append("text")
     .attr("class", "about lifespan")
    .attr("x", function(d) { return d.x; })
    .attr("y", function(d) { return 14 + height - d.y; })
    .style("text-anchor", "middle")
    .text(function(d) { return d.date; });

node.append("text")
     .attr("class", "about lifespan")
    .attr("x", function(d) { return d.x; })
    .attr("y", function(d) { return 28 + height - d.y; })
    .style("text-anchor", "middle")
    .text(function(d) { return d.location; });

var link = svg.selectAll(".link")
    .data(tree.links(nodes))
   .enter()
    .insert("path", "g")
    .attr("fill", "none")
    .attr("stroke", "#000")
    .attr("stroke", "#000")
    .attr("shape-rendering", "crispEdges")
    .attr("d", connect);

function connect(d, i) {
    return     "M" + d.source.x + "," + (height - d.source.y)
             + "V" + (height - (3*d.source.y + 4*d.target.y)/7)
             + "H" + d.target.x
             + "V" + (height - d.target.y);
};