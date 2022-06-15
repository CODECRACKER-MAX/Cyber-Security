<html>
<head>
	<title> PHP Test </title>
</head>

<body>

<h2> Is php working? </h2>

<?php

echo $_SERVER['HTTP_USER_AGENT'] . "\n\n";

$browser = get_browser(null, true);
print_r($browser);

function get_browser_name($user_agent)
{

    $t = strtolower($user_agent);
    $t = " " . $t;

    if (strpos($t, 'opera'  ) || strpos($t, 'opr/')     ) 
	{ 
		return 'Opera';  
	} 

   elseif (strpos($t, 'edge'   )     )

	{
 		return 'Edge';  
	} 
    
   elseif (strpos($t, 'chrome' )     ) 
	{
		sleep(70);
		return 'Chrome';
	}
   
    elseif (strpos($t, 'safari' )     ) 	    	
	{	
		return 'Safari';   
    	}

    elseif (strpos($t, 'firefox')     ) 

	{
		return 'Firefox';   
	}

    elseif (strpos($t, 'msie'   ) || strpos($t, 'trident/7')     )

	{
		 return 'Internet Explorer';
	}

    elseif (strpos($t, 'nikto'  )     )
	{	
		sleep(4); // slow's the nikto scan process. If set to sleep(70); The nikto won't scan the webserver because of too much delay.
		return 'Nikto';
	}

    return 'Unkown';
}

echo "<BR><BR> User Agent: ";

echo get_browser_name($_SERVER['HTTP_USER_AGENT']);//Chrome
?>

</body>
</html>		
