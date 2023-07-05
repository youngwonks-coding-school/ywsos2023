import 'package:dio/dio.dart';
import 'package:localstorage/localstorage.dart';

class API {
  static final API _singleton = API._internal();

  factory API() {
    if (!_singleton._loaded) {
      _singleton._loaded = true;
      if (_singleton.storage.getItem("refreshToken") != null) {
        _singleton._loggedIn = true;
        _singleton.verify();
      }
    }
    return _singleton;
  }

  API._internal();

  static const serverURL = 'http://192.168.1.23:5000';

  final dio = Dio();
  final storage = LocalStorage('auth.json');

  bool _loggedIn = false;
  bool _loaded = false;

  Future<Response?> register(
      String email, String password, bool isRestaurant) async {
    try {
      Response response = await dio.post(
        '$serverURL/api/auth/register',
        data: {
          'email': email,
          'password': password,
          'business_type': isRestaurant ? 'Restaurant' : 'Food Bank'
        },
        options: Options(
          validateStatus: (status) {
            return status! < 500;
          },
        ),
      );

      if (response.statusCode == 409) {
        return response;
      }

      await storage.setItem('refreshToken', response.data['refresh_token']);
      await storage.setItem('accessToken', response.data['access_token']);
      await storage.setItem('email', email);

      _loggedIn = true;

      return response;
    } on DioException catch (ex) {
      if (ex.type != DioExceptionType.connectionTimeout) {
        throw Exception(ex.message);
      }

      return null;
    }
  }

  Future<Response?> login(String email, String password) async {
    try {
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
        await storage.setItem('refreshToken', response.data['refresh_token']);
        await storage.setItem('accessToken', response.data['access_token']);
        await storage.setItem('email', email);

        _loggedIn = true;
      }

      return response;
    } on DioException catch (ex) {
      if (ex.type != DioExceptionType.connectionTimeout) {
        throw Exception(ex.message);
      }

      return null;
    }
  }

  Future<Map?> verify() async {
    if (await storage.getItem('refreshToken') == null) {
      return null;
    }

    Response response;

    try {
      response = await dio.post(
        '$serverURL/api/auth/verify',
        options: Options(
          headers: {
            'Authorization': 'Bearer ${await storage.getItem('accessToken')}'
          },
          validateStatus: (status) {
            return status! < 500;
          },
        ),
      );
    } on DioException catch (ex) {
      if (ex.type != DioExceptionType.connectionTimeout) {
        throw Exception(ex.message);
      }

      return {
        "error": "The server was unable to be reached! Please try again later."
      };
    }

    if (response.statusCode != 200) {
      Response refreshResponse = await dio.post(
        '$serverURL/api/auth/refresh',
        options: Options(
          headers: {
            'Authorization': 'Bearer ${await storage.getItem('refreshToken')}'
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

    return null;
  }

  Future<void> logout() async {
    await dio.post(
      '$serverURL/api/auth/logout',
      options: Options(
        headers: {
          'Authorization': 'Bearer ${await storage.getItem('refreshToken')}'
        },
        validateStatus: (status) {
          return status! < 500;
        },
      ),
    );
    await storage.deleteItem('refreshToken');
    await storage.deleteItem('accessToken');
    await storage.deleteItem('email');
    _loggedIn = false;
  }

  bool loggedIn() {
    return _loggedIn;
  }

  Future<Response> getPosts() async {
    return await dio.get('$serverURL/api/posts/get-posts');
  }

  Future<Response> createPost(
      {required String title,
      required String description,
      required String location}) async {
    Response response = await dio.post(
      '$serverURL/api/posts/create-post',
      data: {
        'title': title,
        'description': description,
        'location': location,
      },
      options: Options(
        headers: {
          'Authorization': 'Bearer ${await storage.getItem('accessToken')}'
        },
        validateStatus: (status) {
          return status! < 500;
        },
      ),
    );

    return response;
  }
}
