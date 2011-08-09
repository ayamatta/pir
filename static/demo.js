$(document).ready(function(){
	
	// third example
	$("#red").treeview({
		animated: "fast",
		collapsed: true,
		unique: false,
		persist: "cookie",
		toggle: function() {
			window.console && console.log("%o was toggled", this);
		}
	});

});