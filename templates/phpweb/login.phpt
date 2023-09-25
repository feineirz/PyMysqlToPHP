<?php
include 'classes/{LOGIN_CLASSNAME}Cls.php';

${LOGIN_TABLENAME_LOWER} = new {LOGIN_CLASSNAME}();
if (isset($_POST['login'])) {
    ${LOGIN_USERNAME_COLUMNNAME} = $_POST['{LOGIN_USERNAME_COLUMNNAME}'];
    ${LOGIN_PASSWORD_COLUMNNAME} = $_POST['{LOGIN_PASSWORD_COLUMNNAME}'];
    $rtrs = ${LOGIN_TABLENAME_LOWER}->Login(${LOGIN_USERNAME_COLUMNNAME}, ${LOGIN_PASSWORD_COLUMNNAME});

    if ($rtrs->Code == 0) {
        ${LOGIN_TABLENAME_LOWER} = $rtrs->Object;
        session_start();
        $_SESSION['{LOGIN_TABLENAME_LOWER}_{LOGIN_TABLENAME_PRIMARY_KEY}'] = ${LOGIN_TABLENAME_LOWER}->{LOGIN_TABLENAME_PRIMARY_KEY};

        header('Location: index.php');
        exit();

    } else {
        echo '<script>alert("ACCESS DENIED!");</script>';
    }
}

include 'head.php';

?>

  <body>

    <div class="container mt-auto mb-auto">
        <div class="row mt-4 mb-4" style="height: 12vh;">&nbsp;</div>

        <div class="row pull-center mt-4">
            <div class="col col-12 pull-center">
                <form action="" method="POST">

                    <div class="card trans-black-80 text-light login-form ms-auto me-auto mt-4 mb-4">
                        <div class="card-header text-light trans-black-70">
                            <h2 class="pt-2"><i class="fas fa-server"></i> {SITE_TITLE}</h2>
                        </div>
                    </div>

                    <div class="card trans-black-80 text-light login-form ms-auto me-auto mt-4 mb-4">
                        <div class="card-header text-success trans-black-80">
                            <h3 class="pt-2"><i class="fas fa-sign-in-alt"></i> SYSTEM LOGIN</h3>
                        </div>
                        <div class="card-body pull-center">
                            <div class="input-group mt-3 mb-3 pull-center w-75 ms-auto me-auto">
                                <span class="input-group-text" id="basic-addon1"><i class="fas fa-user-circle"></i></span>
                                <input name="{LOGIN_USERNAME_COLUMNNAME}" type="text" class="form-control" placeholder="{LOGIN_USERNAME_COLUMNNAME_FIRSTCAP}" aria-label="{LOGIN_USERNAME_COLUMNNAME_FIRSTCAP}" aria-describedby="basic-addon1">
                            </div>
                            <div class="input-group mb-3 pull-center w-75 ms-auto me-auto">
                                <span class="input-group-text" id="basic-addon1"><i class="fas fa-key"></i></span>
                                <input name="{LOGIN_PASSWORD_COLUMNNAME}" type="password" class="form-control" placeholder="{LOGIN_PASSWORD_COLUMNNAME_FIRSTCAP}" aria-label="{LOGIN_PASSWORD_COLUMNNAME_FIRSTCAP}" aria-describedby="basic-addon1">
                            </div>
                        </div>
                        <div class="card-footer pull-center trans-black-80">
                            <button class="btn btn-success" type="submit" name="login"><i class="fas fa-sign-in-alt"></i> LOGIN</button>
                        </div>
                    </div>

                </form>
            </div>
        </div>

    </div>
    

    <?php include 'footer.php'; ?>
    
  </body>
</html>
