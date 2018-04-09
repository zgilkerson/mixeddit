import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Location } from '@angular/common';

@Injectable()
export class SpotifyService {

  api = 'spotify/';

  constructor(private http: HttpClient,
              private location: Location) { }

  getLoggedIn() {
    return this.http.get(this.location.prepareExternalUrl(this.api + 'check_logged_in'));
  }
}
