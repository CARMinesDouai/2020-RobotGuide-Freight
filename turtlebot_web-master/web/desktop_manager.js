var desktop_sup = function(a){
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
  this.supress = function(desktop_toSup){
	
	var dropDownElement = document.getElementById('monselect');
	var UserSelection = dropDownElement.options[dropDownElement.selectedIndex].value;
	console.log(UserSelection)
	desktop_toSup.desktop_to_erase(UserSelection)
	/*alert(" If you just want value ==>" + document.getElementById('dropDownMenu').innerHTML); */
	
  };
  this.desktop_to_erase = function (desktop_selected) {
    //console.log(JSON.stringify(desktop_clicked.value));
    var sup_Publisher = new ROSLIB.Topic({
      ros : ros,
      name : '/desktop_name_to_supress',
      messageType : 'projet_fetch/desktop_name'
    });
    var desktopToSup = new ROSLIB.Message({
	//desktop_name: 'desktop_clicked'
	desktop_name: desktop_selected
    });
    console.log(desktop_selected);
    for (var a=0; a<10; a++) {
    	sup_Publisher.publish(desktopToSup);
    };
  };
};


