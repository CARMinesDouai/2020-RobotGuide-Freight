var new_desktop = false;
var desktop_counter = 0;

var Desktop = function (a) {
  var that  = this;
  this.ros  = a.ros;
  this.continuous = a.continuous || false;
  this.divID = a.divID || 'map';
  this.withOrientation = a.withOrientation || true;
  this.showPath = a.showPath || false;
  this.serverName = a.serverName || '/move_base';
  this.actionName = a.actionName || 'move_base_msgs/MoveBaseAction';
  this.navServerName = a.navServerName || '/move_base/NavfnROS/plan';
  this.navActionName = a.navActionName || 'nav_msgs/Path';


  this.setGoal = function (desktop_clicked) {
    //console.log(JSON.stringify(desktop_clicked.value));
    
    var deskName = new ROSLIB.Topic({
      ros : ros,
      name : '/desktop_to_reach_name',
      messageType : 'projet_fetch/desktop_name'
    });
    var desktopToReach = new ROSLIB.Message({
	//desktop_name: 'desktop_clicked'
	desktop_name: desktop_clicked.value
    });
    console.log(desktop_clicked);
    for (var a=0; a<10; a++) {
    	deskName.publish(desktopToReach);
    };
  };

  this.getDesktopNames = function (){
    var desktop_name_list = new ROSLIB.Topic({
      ros : that.ros,
      name : '/desktop_name_data',
      messageType : 'projet_fetch/desktop_name_list'
    });
    ma_fonction = function(data) {   
	      that.data = data;
	      that.desktop_list = data.desktop_list;
	      that.desktop_nb_data = data.desktop_list.length;
	      //console.log(data.desktop_list);
	  var totalButtons = data.desktop_list.length;
	  console.log(totalButtons);
	  if (desktop_counter != totalButtons){
		  desktop_counter = totalButtons;
		  var navButtons = document.getElementById("nav-buttons");
		  for (var b=0; b<totalButtons;b++){
		  	  var button = document.createElement("button");
			  console.log(button);
			  button.setAttribute("value", that.desktop_list[b]);
			  button.setAttribute("class", "btn");
			  button.setAttribute("tyoe", "button");
			  button.setAttribute("onclick", "desktop.setGoal(this)");
			  //button.innerHTML="Desktop " + b;
			  button.innerHTML= that.desktop_list[b];
			  navButtons.appendChild(button);  
			  };
		  var optionsMenu = document.getElementById("monselect");
		  for (var b=0; b<totalButtons;b++){
		  	  var opt = document.createElement('option');
			  opt.setAttribute("value", that.desktop_list[b]);
			  opt.setAttribute("label", that.desktop_list[b]);
			  //button.innerHTML="Desktop " + b;
			  opt.innerHTML= that.desktop_list[b];
			  optionsMenu.appendChild(opt); 
			  };
	 	 };
	  desktop_name_list.unsubscribe();
	  };

	  
  desktop_name_list.subscribe(ma_fonction);
  };
};

