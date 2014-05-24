
        var margin = {top: 10, right: 220, bottom: 0, left: 0},
            width = 550 - margin.left - margin.right,
            height = 400 - margin.top - margin.bottom;

        var tree = d3.layout.tree()
            .separation(function(a, b) { return a.parent === b.parent ? 1 : .5; })
            .children(function(d) { return d.parents; })
            .size([height, width]);

        var svg = d3.select("#graph2").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        //var myjson = '{  "name": "Clifford Shanks",  "born": 1862,  "married": 1880,  "died": 1906,  "location": "Petersburg, VA",  "parents":[]}';
        var myjson = '{{json_dict|tojson|safe}}';

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
              .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; })

          node.append("text")
              .attr("class", "name")
              .attr("x", 8)
              .attr("y", -6)
              .text(function(d) { return d.fname + ' ' + d.lname; });

          node.append("text")
              .attr("class", "name")
              .attr("x", 8)
              .attr("y", -6)
              .attr("dy", "-1.4em")
              .text(function(d) { return d.id ? '(' + d.id + ')' : ''; });

          node.append("text")
              .attr("x", 8)
              .attr("y", 8)
              .attr("dy", ".71em")
              .attr("class", "about lifespan")
              .text(function(d) { return d.date; });
              //.text(function(d) { return d.born + "–" + d.married + '-' + d.died; });

          node.append("text")
              .attr("x", 8)
              .attr("y", 8)
              .attr("dy", "1.86em")
              .attr("class", "about location")
              .text(function(d) { return d.location; });


        //});

        function elbow(d, i) {
          return "M" + d.source.y + "," + d.source.x
               + "H" + d.target.y + "V" + d.target.x
               + (d.target.children ? "" : "h" + margin.right);
        }
