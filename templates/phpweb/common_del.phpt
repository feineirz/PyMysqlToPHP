<?php
session_start();

include 'classes/{TABLE_NAME_FIRSTCAP}Cls.php';

${TABLE_NAME_LOWER} = new {TABLE_NAME_FIRSTCAP}();
$rtrs = new {TABLE_NAME_FIRSTCAP}ReturnResult();

if($_SESSION['{LOGIN_TABLENAME_LOWER}_{LOGIN_TABLENAME_PRIMARY_KEY}']){
    $ss_{LOGIN_TABLENAME_LOWER}_{LOGIN_TABLENAME_PRIMARY_KEY} = $_SESSION['{LOGIN_TABLENAME_LOWER}_{LOGIN_TABLENAME_PRIMARY_KEY}'];

    $cid = $_GET['cid'];
    if ($cid) {
        ${TABLE_NAME_LOWER} = new {TABLE_NAME_FIRSTCAP}($cid);
    }

    include 'head.php';
?>
<!-- *No tag <Body>...</Body> just body contents -->
    <div class="x-container mt-4">
        <div class="row pull-center">
            <div class="col col-12 col-md-3"></div>
            <div class="col col-12 col-md-6">
                <div class="card common-card text-light">
                    <div class="card-header h3 common-card text-dark">
                        <span>DELETION CONFIRM</span>
                    </div>
                    <?php
                        $submit = $_POST['submit'];
                        $cid = $_POST['cid'];
                        if ($submit) {
                            if ($submit == 'CONFIRM') {
                                ${TABLE_NAME_LOWER}->Delete(($cid));
                            }
                            header('Location: {TABLE_NAME_LOWER}_mgr.php');
                        }
                    ?>

                    <div class="card-body  trans-darkpurple-80">
                        <p>
                            Are you sure to PERMANENTLY DELETE <br/><br/>
                            &nbsp;&nbsp;&nbsp;{DELETE_MESSAGE}?
                        </p>
                    </div>
                    <form action="" name="del_{TABLE_NAME_LOWER}" method="POST">
                        <div class="card-footer common-card text-dark">
                            <input type="submit" name="submit" class="btn btn-danger" value="CONFIRM"></input>
                            <input type="submit" name="submit" class="btn btn-warning" value="CANCEL"></input>
                            <input type="hidden" name="cid" value="<?=${TABLE_NAME_LOWER}->id?>">
                        </div>
                    </form>

                </div>
            </div>
            <div class="col col-12 col-md-3"></div>
        </div>
    </div>

<?php
    include 'footer.php';

}else{
    header("Location: login.php");
    exit();
}
?>