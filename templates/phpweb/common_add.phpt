<?php
include 'classes/{TABLE_NAME_FIRSTCAP}Cls.php';
include 'classes/HelperCls.php';

$helper = new Helper();

session_start();
if($_SESSION['{LOGIN_TABLENAME_LOWER}_{LOGIN_TABLENAME_PRIMARY_KEY}']){
    $ss_{LOGIN_TABLENAME_LOWER}_{LOGIN_TABLENAME_PRIMARY_KEY} = $_SESSION['{LOGIN_TABLENAME_LOWER}_{LOGIN_TABLENAME_PRIMARY_KEY}'];
    include 'head.php';

    $mode = 'add';
    if ($_GET['mode']) {
        $mode = $_GET['mode'];
        $cid = $_GET['cid'];
        if ($mode == 'edit' && $cid) {
            ${TABLE_NAME_LOWER} = new {TABLE_NAME_FIRSTCAP}($cid);
        }
    }
    
    if (isset($_FILES)) {
        {UPLOAD_LIST_CONTENT}
    }

    $submit = $_POST['submit'];
    if ($submit) {
        if($submit == 'ADD {TABLE_NAME_UPPER}'){
            ${TABLE_NAME_LOWER}_info = new {TABLE_NAME_FIRSTCAP}Info();
            // Prepare value{ADD_PARAMS_CONTENT}

            ${TABLE_NAME_LOWER} = new {TABLE_NAME_FIRSTCAP}();
            $rtrs = ${TABLE_NAME_LOWER}->Add(${TABLE_NAME_LOWER}_info);
            if ($rtrs->Code == 0) header('Location: {TABLE_NAME_LOWER}_mgr.php');
        } else if($submit == 'UPDATE'){
            ${TABLE_NAME_LOWER} = new {TABLE_NAME_FIRSTCAP}($_POST['{TABLE_PRIMARY_KEY}']);
            if (${TABLE_NAME_LOWER}) {{UPDATE_PARAMS_CONTENT}
            }
            header('Location: {TABLE_NAME_LOWER}_mgr.php');
        } else if ($submit == 'CANCEL') {
            header('Location: {TABLE_NAME_LOWER}_mgr.php');
        }
    }    

?>
<!-- *No tag <Body>...</Body> just body contents -->
    
    <div class="t-container">
        <div class="row mt-2">
            <!-- Header -->
            <div class="col col-12 mb-2 text-dark trans-white-0 section-header">
                <div class="card ml-2 mt-2 round-box-5">
                    <div class="card-body pull-center pull-middle common-card rounded-box-5 text-dark h1">
                        {TABLE_NAME_UPPER}
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col col-12 mb-2 text-dark trans-white-0">
                <div class="card ml-2 mt-2 common-card">
                    <div class="card-header pull-center pull-middle common-card text-dark h3">
                    <?php echo $mode == 'add'? 'Add New {TABLE_NAME_FIRSTCAP}' : 'Edit {TABLE_NAME_FIRSTCAP} Info' ?>
                    </div>
                    <div class="card-body pull-center pull-middle trans-darkpurple-60 text-dark">
                        <form action="<?=$_SERVER['PHP_SELF']?>" name="add_{TABLE_NAME_LOWER}" method="POST"  enctype="multipart/form-data">
                            <div class="row">
                                
                                <div class="col col-12 col-md-8 ms-auto me-auto col-lg-6">         
                                    <?php if ($rtrs->Code > 0) {?>  
                                    <p class="danger-label"><?=$rtrs->Message?></p>
                                    <?php }?>                           
                                    <div class="card trans-darkpurple-60">
                                        <div class="card-header trans-darkpurple-80 pull-left text-light h6">
                                            {TABLE_NAME_FIRSTCAP} Info
                                        </div>
                                        <div class="card-body trans-darkpurple-30 text-light">
                                            <div class="row">
                                                <input type="hidden" name="id" value="<?=$cid?>">
                                                {ADD_INPUTS_CONTENT}
                                                
                                            </div>
                                        </div>
                                        <div class="card-footer trans-darkpurple-80">                                            
                                            <input class="btn btn-success" type="submit" name="submit" value="<?php echo $mode == 'add'? 'ADD {TABLE_NAME_UPPER}' : 'UPDATE'?>">
                                          
                                            <a href="{TABLE_NAME_LOWER}_mgr.php">
                                                <span class="btn btn-warning">CANCEL</span>
                                            </a>
                                        </div>
                                    </div>
                                </div>

                            </div>
                        </form>  
                    </div>
                    <div class="card-footer pull-center pull-middle common-card rounded-box-5 footer-content min-height-5">
                        {FOOTER_CREDITS}
                    </div>
                </div>
            </div>
        </div>


    </div>


<?php
    include 'footer.php';

}else{
    header("Location: login.php");
    exit();
}
?>