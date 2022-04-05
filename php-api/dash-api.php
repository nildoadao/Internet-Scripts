<?php
include('config.php');

$connection = null;

function build_connection(){
    global $connection;

    try{
        $connection = new mysqli(DB_HOST,DB_USERNAME,DB_PASSWORD,DB_DATABASE_NAME);
        if (mysqli_connect_errno()){
            echo "Falha ao conectar no banco" . mysqli_connect_error();
            http_response_code(500);
            exit();
        }
    } catch (Exception $e){
        echo "Falha ao conectar no banco" . $e->getMessage();
        http_response_code(500);
        exit();
    }
}

function close_connection(){
    global $connection;

    if($connection != null){
        mysqli_close($connection);
    }
}

switch ($_SERVER["REQUEST_METHOD"]){
    case 'GET':
        if($_GET['server_id'] != ""){
            $result = get_server_by_id($_GET['server_id']);
            $response_data = json_encode($result);
            echo $response_data;
            close_connection();
        }
        break;
        
    default:
        http_response_code(400);
        echo "Solicitação mal formatada";
        close_connection();
        break;
}

function execute_query($query = "", $params = []){
    global $connection;

    try{
        $statement = $connection->prepare($query);

        if($statement === false){
            echo "Falha ao conectar no banco";
            http_response_code(500);
            exit();
        }

        if($params){
            $statement->bind_param($params[0], $params[1]);
        }
        
        $statement->execute();
        $result = $statement->get_result()->fetch_all(MYSQLI_ASSOC);
        $statement->close();
        return $result;

    } catch(Exception $e) {
        echo "Falha ao conectar no banco" . $e->getMessage();
        http_response_code(500);
        exit();
    } 
}

function get_server_by_name($server_name){
    global $connection;

    if ($connection == null){
        build_connection();
    }

    $query = "SELECT * FROM hostdb WHERE hostname=?";
    $params = ["i", $server_name];
    return execute_query($query, $params);
}

function get_server_by_id($server_id){
    global $connection;

    if ($connection == null){
        build_connection();
    }

    $query = "SELECT * FROM hostdb WHERE id=?";
    $params = ["i", $server_id];
    return execute_query($query, $params);
}

?>