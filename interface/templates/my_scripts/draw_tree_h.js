/***********************
GUIDELINE on SVG text element:
    http://www.w3.org/TR/SVG/paths.html#PathData
***********************/



var tree = d3.layout.tree()
.separation(function(a, b) { return a.parent === b.parent ? 1 : .5; })
.children(function(d) { return d.parents; })
.size([height, width]);



//var myjson = '{  "name": "Clifford Shanks",  "born": 1862,  "married": 1880,  "died": 1906,  "location": "Petersburg, VA",  "parents":[]}';

json = JSON.parse( myjson )
//d3.json("{{ url_for('static',filename = 'd3/tree.json')}}", function(json) {
var nodes = tree.nodes(json);

var link = svg.selectAll(".link")
  .data(tree.links(nodes))
  .enter().append("path")
  .attr("class", "link")
  .attr("d", elbow);

var node = svg.selectAll(".node")
  .data(nodes)
  .enter().append("g")
  .attr("class", "node")
  .attr("transform", function(d) { return "translate(" +  (width - (d.born ? -margin.right:0)  - d.y) + "," +  d.x + ")"; })


node.append("text")
  .attr("class", function(d) { return d.selected?"selected":"name";})
  .attr("x", -3)
  .attr("y", -5)
  .attr("text-anchor", "end")
  .text(function(d) { return d.fname + ' ' + d.lname; });



node.append("text")
  .attr("x", -3)
  .attr("y", 5)
  .attr("dy", ".71em")
  .attr("class", "about lifespan")
  .attr("text-anchor","end")
  .text(function(d) { return (d.id? '(#' + d.id + ') ' : ''); });

node.append("text")
  .attr("x", -3)
  .attr("y", 6)
  .attr("dy", "1.86em")
  .attr("class", "about lifespan")
  .attr("text-anchor","end")
  .text(function(d) { return d.date;} );

node.append("text")
  .attr("x", -3)
  .attr("y", 7)
  .attr("dy", "2.96em")
  .attr("class", "about location")
  .attr("text-anchor","end")
  .text(function(d) { return d.location; });



// guideline on paths: http://tutorials.jenkov.com/svg/text-element.html
function elbow(d, i) {
return "M" + (width - d.source.y) + "," + d.source.x
   + "H" + (width - d.target.y) + "V" + d.target.x
   + (d.target.children ? "" : "h" + ( -.8 * margin.left));
}



/*  Here is the original right to left tree drawing
function elbow(d, i) {
return "M" + d.source.y + "," + d.source.x
   + "H" + d.target.y + "V" + d.target.x
   + (d.target.children ? "" : "h" + margin.right);
}
*/