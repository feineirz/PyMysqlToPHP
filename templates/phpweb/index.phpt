<?php
session_start();

if ($_POST['logout']) {
    session_destroy();
    header("Location: login.php");
    exit();
}

if($_SESSION['{LOGIN_TABLENAME_LOWER}_{LOGIN_TABLENAME_PRIMARY_KEY}']){

{INCLUDE_ALL_CLASSES}{ROW_COUNT_CONTENT}
    $ss_{LOGIN_TABLENAME_LOWER}_{LOGIN_TABLENAME_PRIMARY_KEY} = $_SESSION['{LOGIN_TABLENAME_LOWER}_{LOGIN_TABLENAME_PRIMARY_KEY}'];
    include 'head.php';
?>

    <div class="x-container mt-2 mb-2">
        <div class="row trans-white-10 pull-center">

            <!-- Header -->
            <div class="col col-12 mb-2 text-dark trans-white-0 section-header">
                <div class="card mt-4 rounded-box-5 common-card">
                    <div class="card-body pull-center pull-middle rounded-box-5 h1">
                        DATABASE MANAGEMENT
                    </div>
                </div>
            </div>
            <div class="col col-12 pull-right text-dark trans-white-0 section-header mb-2">
                <form action="<?php echo $_SERVER['PHP_SELF']; ?>" name="logout" method="POST">
                    <button type="submit" class="btn btn-danger" name="logout" value="logout">LOGOUT <i class="fas fa-sign-out-alt"></i></button>
                </form>
            </div>
{INDEX_MENU_CARDS}
            
            <!-- Footer -->
            <div class="col col-12 mb-4 text-dark trans-white-0 section-header">
                <div class="card ml-2 rounded-box-5">
                    <div class="card-body pull-center pull-middle common-card rounded-box-5 footer-content min-height-5">
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
