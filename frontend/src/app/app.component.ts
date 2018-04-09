import { Component, OnInit, Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Observable } from 'rxjs/Observable';

import 'rxjs/add/operator/toPromise';

import { SpotifyService } from './spotify.service';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers: [SpotifyService]
})

@Injectable()
export class AppComponent implements OnInit {
  title = 'app';
  logged_in = false;

  constructor(private spotify: SpotifyService) {}

  ngOnInit() {
    this.spotify.getLoggedIn().subscribe(
      (data) => this.logged_in = true,
      (error: HttpErrorResponse) => this.logged_in = false
    );
  }
}
