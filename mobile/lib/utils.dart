import 'package:custom_navigation_bar/custom_navigation_bar.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'api_interface.dart';

Widget buildNavbar({
  required Color selectedColor,
  required Color unSelectedColor,
  required int currentPageIndex,
  required List<String> routes,
  required BuildContext context,
}) {
  return CustomNavigationBar(
    iconSize: 30.0,
    selectedColor: selectedColor,
    strokeColor: const Color(0x30040307),
    unSelectedColor: unSelectedColor,
    backgroundColor: Colors.white,
    items: [
      CustomNavigationBarItem(
        icon: const Icon(CupertinoIcons.home),
        title: Text(
          "Home",
          style: TextStyle(
              color: currentPageIndex == 0 ? selectedColor : unSelectedColor),
        ),
      ),
      CustomNavigationBarItem(
        icon: const Icon(Icons.hiking_outlined),
        title: Text(
          "Discover",
          style: TextStyle(
            color: currentPageIndex == 1 ? selectedColor : unSelectedColor,
          ),
        ),
      ),
      CustomNavigationBarItem(
        icon: const Icon(CupertinoIcons.map),
        title: Text(
          "Map",
          style: TextStyle(
            color: currentPageIndex == 2 ? selectedColor : unSelectedColor,
          ),
        ),
      ),
      CustomNavigationBarItem(
        icon: const Icon(CupertinoIcons.person_crop_circle),
        title: Text(
          API().loggedIn() ? "Profile" : "Auth",
          style: TextStyle(
            color: currentPageIndex == 3 ? selectedColor : unSelectedColor,
          ),
        ),
      ),
    ],
    currentIndex: currentPageIndex,
    onTap: (index) {
      if (API().loggedIn()) {
        if (index == 3) {
          index = 4;
        }
      }
      Navigator.pushNamed(context, routes[index]);
    },
  );
}

PreferredSizeWidget appbarComponent({required String title}) {
  return AppBar(
    automaticallyImplyLeading: false,
    backgroundColor: Colors.transparent,
    elevation: 0,
    title: Row(
      children: [
        Padding(
          padding: const EdgeInsets.only(top: 15),
          child: Text(
            title,
            style: const TextStyle(
              color: Color.fromRGBO(121, 45, 65, 1),
              fontSize: 40,
            ),
          ),
        ),
      ],
    ),
  );
}

TextField buildTextField(
    {required String labelText,
    required TextEditingController controller,
    required bool obscureText,
    required IconData icon,
    required BuildContext context}) {
  return TextField(
    controller: controller,
    obscureText: obscureText,
    decoration: InputDecoration(
      prefixIcon: Icon(icon),
      labelText: labelText,
      isDense: true,
      labelStyle: const TextStyle(fontSize: 17),
      enabledBorder: const OutlineInputBorder(
        borderRadius: BorderRadius.all(Radius.circular(10.0)),
        borderSide: BorderSide(
          color: Colors.grey,
        ),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: const BorderRadius.all(Radius.circular(10.0)),
        borderSide: BorderSide(color: Theme.of(context).primaryColor),
        // borderSide: BorderSide(color: Color.fromRGBO(187, 170, 159, 1)),
      ),
    ),
  );
}
