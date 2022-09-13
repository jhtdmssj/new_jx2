<!DOCTYPE html>
<!--[if IE 8]> <html lang="en" class="ie8"> <![endif]-->
<!--[if IE 9]> <html lang="en" class="ie9"> <![endif]-->
<!--[if !IE]><!--><html lang="en"> <!--<![endif]-->
<!-- BEGIN HEAD -->
<head>
	<meta charset="utf-8" />
	<title>KWPO3</title>
	<meta content="width=device-width, initial-scale=1.0" name="viewport" />
	<meta content="" name="description" />
	<meta content="" name="author" />
	<link href="assets/bootstrap/css/bootstrap.min.css" rel="stylesheet" />
	<link href="assets/bootstrap/css/bootstrap-responsive.min.css" rel="stylesheet" />
	<link href="assets/font-awesome/css/font-awesome.css" rel="stylesheet" />
	<link href="css/style.css" rel="stylesheet" />
	<link href="css/style_responsive.css" rel="stylesheet" />
	<link href="css/style_default.css" rel="stylesheet" id="style_color" />
	<link href="assets/fancybox/source/jquery.fancybox.css" rel="stylesheet" />
	<link rel="stylesheet" type="text/css" href="assets/uniform/css/uniform.default.css" />
	<link href="assets/fullcalendar/fullcalendar/bootstrap-fullcalendar.css" rel="stylesheet" />
	<link href="assets/jqvmap/jqvmap/jqvmap.css" media="screen" rel="stylesheet" type="text/css" />
	<style>
    body{ background:none!important}
    </style>
</head>

<body class="fixed-top">

<div id="page" class="dashboard">
    <div class="row-fluid">
        <div class="span12">
            <div class="widget">
                <div class="widget-title">
                    <h4><i class="icon-tags"></i> 电信数据 上传1</h4>
                        <span class="tools">
                        <a href="javascript:;" class="icon-chevron-down"></a>
                        <a href="javascript:;" class="icon-remove"></a>
                        </span>
                </div>
                <div class="widget-body">
                		<form id="upload" action="upload2.php" method="post" enctype="multipart/form-data">
                    	<table class="table table-striped table-bordered table-advance table-hover">
                                        <thead>
                                        <tr>
                                            <th><i class="icon-leaf"></i> <span class="hidden-phone">文件名称</span></th>
                                            <th><i class="icon-user"></i> <span class="hidden-phone ">选择上传文件</span></th>
                                            <th><i class="icon-tags"> </i><span class="hidden-phone">操作</span></th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        <tr>
                                            <td width="500">
                                             电信数据上传文件名称自动生成
                                            </td>
                                            <td>
                                            	<input type="file" name="upfile" /> 
                                            </td>
                                            <td>
                                                <input type="submit" class="btn btn-success" name="submit" value="上传">
                                            </td>
                                        </tr>
                                        </tbody>
                        </table>
                        </form>    


                        <form id="upload" action="upload3.php" method="post" enctype="multipart/form-data">
                        <table class="table table-striped table-bordered table-advance table-hover">
                                        <thead>
                                        <tr>
                                            <th><i class="icon-leaf"></i> <span class="hidden-phone">文件名称</span></th>
                                            <th><i class="icon-user"></i> <span class="hidden-phone ">选择上传文件</span></th>
                                            <th><i class="icon-tags"> </i><span class="hidden-phone">操作</span></th>
                                        </tr>
                                        </thead>
                                        <tbody>
                                        <tr>
                                            <td width="500">
                                             新版电信
                                            </td>
                                            <td>
                                                <input type="file" name="upfile" /> 
                                            </td>
                                            <td>
                                                <input type="submit" class="btn btn-success" name="submit" value="上传">
                                            </td>
                                        </tr>
                                        <tr>
                                            <td colspan="3">
                                                    去掉表的标题头。直接上传即可
                                                    例：魅族    M971Q   2019/4/2    6.0 to 6.4  6.2 2232    1080                    151.9   73.4    android YES
                                            </td>
                                        </tr>
                                        </tbody>
                        </table>
                        </form>        

  
                </div>
            </div>
        </div>

    </div>
</div>
</body>
<script src="js/jquery-1.8.3.min.js"></script>
<script src="assets/jquery-slimscroll/jquery-ui-1.9.2.custom.min.js"></script>
<script src="assets/jquery-slimscroll/jquery.slimscroll.min.js"></script>
<script src="assets/fullcalendar/fullcalendar/fullcalendar.min.js"></script>
<script src="assets/bootstrap/js/bootstrap.min.js"></script>
<script src="js/jquery.blockui.js"></script>
<script src="js/jquery.cookie.js"></script>

</html>