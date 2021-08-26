/*
*   A Tree diagram shows the total utilisation of a resource,
*   In this case, we are interested in what percentage of transactions
*   Related to each category of transaction, at this juncture
*   Shulkers, Rockets, Building Blocks and Other are the main categories
*/

//Object for the bounds and dimensions of the SVG
const tree_margin = {top: 10, right: 10, bottom: 10, left: 10},
  tree_width = 700 - tree_margin.left - tree_margin.right,
  tree_height = 850 - tree_margin.top - tree_margin.bottom;

//Grabs the div with the id of treemap and creates a new SVG inside of it
const tree_svg = d3.select("#treemap")
.append("svg")
  .attr("width", tree_width + tree_margin.left + tree_margin.right)
  .attr("height", tree_height + tree_margin.top + tree_margin.bottom)
.append("g")
  .attr("transform",
        `translate(${tree_margin.left}, ${tree_margin.top})`);
// read json data
d3.json("/assets/data/treemap.json").then(function(data) {
  /*
  *   The data is in the format of cummulative total of transactions per category
  *   We create a hierarchy D3 object to hold the summation of each category, for now each category is singular so is its own sum in the data 
  *   
  */
  const root = d3.hierarchy(data).sum(function(d){ return d.value}) // Here the size of each leave is given in the 'value' field in input data

  // Then d3.treemap computes the position of each element of the hierarchy
  d3.treemap()
    .size([tree_width, tree_height])
    .padding(3)
    (root)

  //Using the d3.treemap object we can create the rectangles for the leaves
  //Color is currently blue determined by the remainder of the transaction / 200
  tree_svg
    .selectAll("rect")
    .data(root.leaves())
    .join("rect")
      .attr('x', function (d) { return d.x0; })
      .attr('y', function (d) { return d.y0; })
      .attr('width', function (d) { return d.x1 - d.x0 + 10; })
      .attr('height', function (d) { return d.y1 - d.y0 + 10; })
      .attr('id','tree-rect')
      .style("stroke", "black")
      .style("fill", function(d) { return "rgb(0, 0, " + (d.data.value % 200) + ")"; })

  //Adding labels to each leaf rect with the category and number of diamonds
  tree_svg
    .selectAll("text")
    .data(root.leaves())
    .join("text")
      .attr("x", function(d){ return d.x0+5})
      .attr("y", function(d){ return d.y0+20})
      .text(function(d){ return d.data.name + " - " + d.data.value})
      .attr("font-size", "15px")
      .attr("fill", "white")
})