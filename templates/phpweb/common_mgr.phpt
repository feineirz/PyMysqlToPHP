<?php
session_start();

include 'classes/{TABLE_NAME_FIRSTCAP}Cls.php';

${TABLE_NAME_LOWER} = new {TABLE_NAME_FIRSTCAP}();
$rtrs = new {TABLE_NAME_FIRSTCAP}ReturnResult();
$item_perpage = 25;
$cur_page = 1;
if ($_GET['page']) $cur_page = $_GET['page'];

$orderby = isset($_POST['orderby'])? $_POST['orderby'] : '{TABLE_PRIMARY_KEY}';
$order_direction = isset($_POST['order_direction'])? ' '.$_POST['order_direction'] : '';
$filter = $_POST['filter'];

$filter_cond = '';
if (!empty(trim($filter))) {
    $filter_cond = ""{SEARCH_CONDITION}
}

if($_SESSION['{LOGIN_TABLENAME_LOWER}_{LOGIN_TABLENAME_PRIMARY_KEY}']){
    $ss_{LOGIN_TABLENAME_LOWER}_{LOGIN_TABLENAME_PRIMARY_KEY} = $_SESSION['{LOGIN_TABLENAME_LOWER}_{LOGIN_TABLENAME_PRIMARY_KEY}'];
    include 'head.php';
?>
<!-- *No tag <Body>...</Body> just body contents -->
    
    <div class="t-container">
        <div class="row mt-2">
            <!-- Header -->
            <div class="col col-12 mb-2 text-dark trans-white-0 section-header">
                <div class="card ml-2 mt-2 rounded-box-5">
                    <div class="card-body pull-center pull-middle common-card rounded-box-5 text-dark h1">
                        {TABLE_NAME_UPPER} MANAGER
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col col-12 mb-2 text-dark trans-white-0">
                <div class="card ml-2 mt-2 common-card">
                    <div class="card-header pull-center pull-middle trans-darkpurple-10 text-dark">
                        <div class="row">
                            <div class="col col-12">
                                <form action="" method="POST">     
                                    <div class="search-container ms-auto">
                                        <div class="search-box">
                                            <span class="me-auto h4">
                                                <a href="index.php"><i class="fas fa-home"></i> </a>
                                            </span>
                                            <label class="inline-label" for="orderby"> | </label>
                                            <label class="inline-label d-block d-md-none" for="orderby">Sort</label> <!-- Mobile -->
                                            <label class="inline-label d-none d-md-block" for="orderby">Sort By</label> <!-- PC -->
                                            <select class="search-cmb" name="orderby" id="orderby">{ORDERBY_CONTENT}
                                            </select>
                                            
                                            <select class="search-cmb" name="order_direction" id="order_direction">
                                                <option value="asc" <?php if($order_direction == ' asc') echo 'selected'; ?>>ASC</option>
                                                <option value="desc" <?php if($order_direction == ' desc') echo 'selected'; ?>>DESC</option>
                                            </select>

                                            <input type="text" class="search" name="filter" placeholder="Search from {TABLE_NAME_FIRSTCAP}" value="<?=$filter?>">
                                            <button type="submit" class="search-btn" name="search" value="search"><i class="fas fa-search"></i></button>
                                            <a href="{TABLE_NAME_LOWER}_add.php">
                                                <button type="button" class="btn btn-success add-btn"><i class="fa fa-plus-circle"></i></button>
                                            </a>
                                        </div>
                                    </div>
                                </form>                                
                            </div>
                        </div>
                    </div>

                    <?php
                    
                    if ($_POST['search']) $cur_page = 1;
                    $rtrs = ${TABLE_NAME_LOWER}->Count($filter_cond);
                    $rec_count = $rtrs->Value;
                    $rtrs = ${TABLE_NAME_LOWER}->ListRows($filter_cond, $_POST['orderby'].''.$order_direction, ($cur_page-1)*$item_perpage, $item_perpage);
                    ${TABLE_NAME_LOWER}_lr = $rtrs->Object;                    
                    ?>

                    <!-- Mobile -->
                    <div class="card-body trans-darkpurple-60 text-light d-block d-lg-none">
                    <?php
                        if (${TABLE_NAME_LOWER}_lr->Count > 0) {
                            foreach (${TABLE_NAME_LOWER}_lr->Items as $item) {
                                ${TABLE_NAME_LOWER} = $item;
                    ?>
                        <div class="card common-card mb-2">
                            <div class="card-header trans-darkpurple-20 text-dark">&nbsp;</div>
                            <div class="card-body trans-white-60 text-dark">{MOBILE_TABLE_CONTENT}
                                <p class="pull-right pt-4">
                                    <a href="{TABLE_NAME_LOWER}_add.php?mode=edit&cid=<?=${TABLE_NAME_LOWER}->id?>">
                                        <button class="btn btn-warning mb-1"><i class="fas fa-edit"></i></button>
                                    </a>
                                    <a href="{TABLE_NAME_LOWER}_del.php?cid=<?=${TABLE_NAME_LOWER}->id?>">
                                        <button class="btn btn-danger mb-1"><i class="fas fa-times-circle"></i></button>
                                    </a>          
                                </p>
                            </div>
                        </div>
                    <?php
                            }
                        }
                    ?>
                    </div>

                    <!-- PC -->
                    <div class="card-body pull-left pull-middle trans-darkpurple-60 text-light d-none d-lg-block min-height-60">                        
                        <table class="table trans-white-80 table-hover rounded-box-5">
                            <thead>
                                <tr>{PC_TABLE_HEADER}
                                    <th class="pull-right" scope="col"><cmd></th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php
                                if (${TABLE_NAME_LOWER}_lr->Count > 0) {
                                    foreach (${TABLE_NAME_LOWER}_lr->Items as $item) {
                                        ${TABLE_NAME_LOWER} = $item;
                                ?>
                                        <tr>{PC_TABLE_CONTENT}
                                            <td class="pull-right">
                                                <a href="{TABLE_NAME_LOWER}_add.php?mode=edit&cid=<?=${TABLE_NAME_LOWER}->id?>">
                                                    <button class="cmd-btn btn-warning mb-1"><i class="fas fa-edit"></i></button>
                                                </a>
                                                <a href="{TABLE_NAME_LOWER}_del.php?cid=<?=${TABLE_NAME_LOWER}->id?>">
                                                    <button class="cmd-btn btn-danger mb-1"><i class="fas fa-times-circle"></i></button>
                                                </a>                                                    
                                            </td>
                                        </tr>        
                                <?php
                                    }
                                }
                                ?>
                            </tbody>
                        </table>
                    </div>

                    <div class="card-footer pull-center pull-middle trans-darkpurple-10 text-light">
                        <?php
                        $page_count = ceil($rec_count / $item_perpage);
                        for ($i = 1; $i <= $page_count; $i++){
                            if ($i == $cur_page) {
                                echo '<span class="btn paginate-box-disable">'.$i.'</span>';
                            } else {
                                echo '<a href="{TABLE_NAME_LOWER}_mgr.php?page='.$i.'"><span class="btn paginate-box">'.$i.'</span></a>';
                            }
                        }
                        ?>
                    </div>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <div class="row mt-2">
            <!-- Header -->
            <div class="col col-12 mb-2 text-dark trans-white-0 section-header">
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