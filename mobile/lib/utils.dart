import 'package:custom_navigation_bar/custom_navigation_bar.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:go_router/go_router.dart';
import 'api_interface.dart';

Widget buildNavbar({
  required BuildContext context,
  required int currentPageIndex,
  Color selectedColor = const Color.fromRGBO(249, 181, 12, 1),
  Color unSelectedColor = const Color.fromRGBO(88, 47, 195, 1),
  List<String>? routes,
}) {
  routes ??= [
    '/',
    '/discover',
    '/posts',
    API().loggedIn() ? '/profile' : '/authenticate'
  ];

  return CustomNavigationBar(
    borderRadius: const Radius.circular(20.0),
    iconSize: 30.0,
    selectedColor: selectedColor,
    strokeColor: const Color(0x30040307),
    unSelectedColor: unSelectedColor,
    backgroundColor: Colors.white,
    items: [
      CustomNavigationBarItem(
        icon: const Icon(CupertinoIcons.home),
        title: Text(
          'Home',
          style: TextStyle(color: unSelectedColor),
        ),
        selectedTitle: Text(
          'Home',
          style: TextStyle(color: selectedColor),
        ),
      ),
      CustomNavigationBarItem(
        icon: const Icon(Icons.hiking_outlined),
        title: Text(
          'Discover',
          style: TextStyle(color: unSelectedColor),
        ),
        selectedTitle: Text(
          'Discover',
          style: TextStyle(color: selectedColor),
        ),
      ),
      CustomNavigationBarItem(
        icon: const Icon(Icons.sticky_note_2_outlined),
        title: Text(
          'Posts',
          style: TextStyle(color: unSelectedColor),
        ),
        selectedTitle: Text(
          'Posts',
          style: TextStyle(color: selectedColor),
        ),
      ),
      CustomNavigationBarItem(
        icon: const Icon(CupertinoIcons.person_crop_circle),
        title: Text(
          API().loggedIn() ? 'Profile' : 'Auth',
          style: TextStyle(
            color: currentPageIndex == 3 ? selectedColor : unSelectedColor,
          ),
        ),
      ),
    ],
    currentIndex: currentPageIndex,
    onTap: (index) {
      context.go(routes![index]);
    },
  );
}

PreferredSizeWidget appbarComponent(
    {required String title, bool backButton = false, PreferredSizeWidget? bottom}) {
  return AppBar(
    automaticallyImplyLeading: backButton,
    bottom: bottom,
    systemOverlayStyle: const SystemUiOverlayStyle(
      statusBarColor: Color.fromRGBO(240, 230, 220, 1),
      statusBarIconBrightness: Brightness.dark,
    ),
    titleSpacing: backButton ? 0 : null,
    flexibleSpace: Container(
      decoration: const BoxDecoration(
        gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: <Color>[
              Color.fromRGBO(240, 230, 220, 1),
              Color.fromRGBO(254, 251, 255, 1)
            ]),
      ),
    ),
    elevation: 0,
    title: Row(
      children: [
        Padding(
          padding: const EdgeInsets.only(top: 15),
          child: Text(
            title,
            style: const TextStyle(
              color: Color.fromRGBO(250, 170, 90, 1),
              fontSize: 48,
            ),
          ),
        ),
      ],
    ),
  );
}

TextFormField buildTextField(
    {required String labelText,
    required IconData icon,
    required BuildContext context,
    TextEditingController? controller,
    bool obscureText = false,
    bool multiline = false,
    bool border = true,
    bool dense = false,
    String? Function(String?)? validate}) {
  return TextFormField(
    controller: controller,
    obscureText: obscureText,
    maxLines: multiline ? null : 1,
    keyboardType: multiline ? TextInputType.multiline : null,
    validator: validate,
    autovalidateMode: validate == null ? AutovalidateMode.disabled : AutovalidateMode.onUserInteraction,
    decoration: InputDecoration(
      prefixIcon: Icon(icon),
      labelText: labelText,
      isDense: true,
      contentPadding: dense ? EdgeInsets.zero : null,
      prefixIconConstraints: dense ? const BoxConstraints(
        minHeight: 40,
        minWidth: 30,
      ) : null,
      labelStyle: const TextStyle(fontSize: 17),
      enabledBorder: border ? const OutlineInputBorder(
        borderRadius: BorderRadius.all(Radius.circular(10.0)),
        borderSide: BorderSide(
          color: Colors.grey,
        ),
      ) : null,
      focusedBorder: border ? OutlineInputBorder(
        borderRadius: const BorderRadius.all(Radius.circular(10.0)),
        borderSide: BorderSide(color: Theme.of(context).primaryColor),
      ) : null,
    ),
  );
}
