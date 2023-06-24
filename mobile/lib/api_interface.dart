import 'package:dio/dio.dart';
import 'package:localstorage/localstorage.dart';

class API {
  static final API _singleton = API._internal();

  factory API() {
    return _singleton;
  }

  API._internal();

  static const serverURL = 'http://192.168.1.23:5000';

  final dio = Dio();
  final storage = LocalStorage('auth.json');

  bool _loggedIn = false;

  Future<Response> register(email, password) async {
    Response response = await dio.post(
      '$serverURL/api/auth/register',
      data: {'email': email, 'password': password},
      options: Options(
        validateStatus: (status) {
          return status! < 500;
        },
      ),
    );

    if (response.statusCode == 409) {
      return response;
    }

    await login(email, password);

    return response;
  }

  Future<Response> login(email, password) async {
    Response response = await dio.post(
      '$serverURL/api/auth/login',
      data: {'email': email, 'password': password},
      options: Options(
        validateStatus: (status) {
          return status! < 500;
        },
      ),
    );

    if (response.statusCode != 401) {
      await storage.setItem('refreshToken', response.data['refreshToken']);
      await storage.setItem('accessToken', response.data['accessToken']);
      await storage.setItem('email', email);

      _loggedIn = true;
    }

    return response;
  }

  void verify() async {
    if (await storage.getItem('refreshToken') == null) {
      return null;
    }
    Response response = await dio.get(
      '$serverURL/api/auth/verify',
      options: Options(
        headers: {
          "Authorization": 'Bearer ${await storage.getItem('refreshToken')}'
        },
        validateStatus: (status) {
          return status! < 500;
        },
      ),
    );

    if (response.statusCode != 200) {
      Response refreshResponse = await dio.get(
        '$serverURL/api/auth/refresh',
        options: Options(
          headers: {
            "Authorization": 'Bearer ${await storage.getItem('refreshToken')}'
          },
          validateStatus: (status) {
            return status! < 500;
          },
        ),
      );

      if (refreshResponse.statusCode != 200) {
        await storage.deleteItem('refreshToken');
        await storage.deleteItem('accessToken');
        await storage.deleteItem('email');
        _loggedIn = false;
      } else {
        await storage.setItem(
            'accessToken', refreshResponse.data['accessToken']);
      }
    }
  }

  Future<void> logout() async {
    await storage.deleteItem('refreshToken');
    await storage.deleteItem('accessToken');
    await storage.deleteItem('email');
    _loggedIn = false;
  }

  bool loggedIn() {
    return _loggedIn;
  }

  Future<Response> getPosts() async {
    Response response = await dio.get('$serverURL/api/get-posts');
    return response;
  }
}
