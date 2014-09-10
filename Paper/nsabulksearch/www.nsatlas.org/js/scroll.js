// onLoad event
window.onload = function(){
    set_scroll();
}
 
// if query string in URL contains scroll=nnn, then scroll position will be restored
function set_scroll(){
    // get query string parameter with "?"
    var search = window.location.search;
    // if query string exists
    if (search){
        scrollx = jQuery.query.get("scrollx");
        scrolly = jQuery.query.get("scrolly");
        window.scrollTo(scrollx, scrolly);
    }
}
 
// append scroll value to the URL
function get_scroll(){
    var scroll;
    // Netscape compliant
  if (typeof(window.pageYOffset) == 'number')
    scroll = window.pageYOffset;
  // DOM compliant
  else if (document.body && document.body.scrollTop)
    scroll = document.body.scrollTop;
  // IE6 standards compliant mode
  else if (document.documentElement && document.documentElement.scrollTop)
    scroll = document.documentElement.scrollTop;
  // needed for IE6 (when vertical scroll bar is on the top)
  else scroll = 0;
    // set href location with scroll position parameter
	return scroll;
}

function saveScrollCoordinates(formnum) { 
   document.forms[formnum].elements['scrolly'].value= get_scroll();
} 
