
use axum::{
    routing::{get, IntoMakeService},
    Router, body::Body,
};
use std::net::SocketAddr;

#[tokio::main]
async fn main() {

    // run our app with hyper
    // `axum::Server` is a re-export of `hyper::Server`
    let addr = SocketAddr::from(([127, 0, 0, 1], 3000));


    let app = make_app_service();
    let server = axum::Server::bind(&addr)
            .serve(app);
    server.await.unwrap();
}

fn make_app_service() -> IntoMakeService<Router<Body>> {
    Router::new()
        // `GET /` goes to `root`
        .route("/", get(root))
        // `POST /users` goes to `create_user`
        .route("/hello", get(hello_world)).into_make_service()
}

// basic handler that responds with a static string
async fn root() -> &'static str {
    "<h1>hello root</h1>\n"
}

// basic handler that responds with a static string
async fn hello_world() -> &'static str {
    "Hello, World!\n"
}

#[cfg(test)]
mod tests {
    use std::net::TcpListener;

    use hyper::Request;

    use super::*;

    #[tokio::test]
    async fn hello() {
        let listener = TcpListener::bind("0.0.0.0:0".parse::<SocketAddr>().unwrap()).unwrap();
        let addr = listener.local_addr().unwrap();

        tokio::spawn(async move {
            axum::Server::from_tcp(listener)
                .unwrap()
                .serve(make_app_service())
                .await
                .unwrap();
        });

        let client = hyper::Client::new();

        let response = client
            .request(
                hyper::Request::builder()
                    .uri(format!("http://{}/hello", addr))
                    .body(Body::empty())
                    .unwrap(),
            )
            .await
            .unwrap();

        let body = hyper::body::to_bytes(response.into_body()).await.unwrap();
        assert_eq!(&body[..], b"Hello, World!\n");
    }
}

