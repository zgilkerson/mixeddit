import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  theme_toggle = new FormControl();

  constructor() {
    this.themeSwitched();
  }

  ngOnInit() {
  }

  themeSwitched() {
    this.theme_toggle.valueChanges.forEach(
      (value: boolean) => document.getElementById('body').classList.toggle('light-theme')
    );
  }
}
