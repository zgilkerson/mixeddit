import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs/Observable';

import 'rxjs/add/operator/toPromise';

import { HttpErrorResponse } from '@angular/common/http';
import { SpotifyService } from '../spotify.service';

@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.scss'],
  providers: [SpotifyService]
})

export class HomepageComponent implements OnInit {

  logged_in = false;

  constructor(private spotify: SpotifyService) {}

  ngOnInit() {
    this.spotify.getLoggedIn().subscribe(
      (data) => this.logged_in = true,
      (error: HttpErrorResponse) => this.logged_in = false
    );
  }

}
