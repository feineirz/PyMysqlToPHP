<?php

    class Helper {
        function extension2type($ext=null) {
            if ($ext == null) {return 'NULL';}
            if (str_contains($ext, 'jpeg')) {return 'images';}
            if (str_contains($ext, 'jpg')) {return 'images';}
            if (str_contains($ext, 'png')) {return 'images';}
            if (str_contains($ext, 'gif')) {return 'images';}
            if (str_contains($ext, 'bmp')) {return 'images';}
            return 'files';
        }        
    }
    
?>
